import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
import re
import os


def scrape_ncbi_coronavirus(start_page=1,end_page=5, max_retries=3):
    """
    Scrape SARS-CoV-2 Nucleocapsid protein data from NCBI's Protein database

    Args:
        start_page (int): First page to scrape
        end_page (int): Last page to scrape
        max_retries (int): Maximum number of retry attempts for each item
    """
    # Set up the webdriver with options
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--start-maximized")
    # Disable GPU acceleration to avoid the GPU error
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-software-rasterizer")
    driver = webdriver.Chrome(options=chrome_options)

    # Navigate directly to SARS-CoV-2 Nucleocapsid protein search results
    print(f"Opening NCBI Protein database for SARS-CoV-2 Nucleocapsid...")
    driver.get("https://www.ncbi.nlm.nih.gov/protein/?term=SARS-CoV-2%5BOrganism%5D+Nucleocapsid")

    # Wait for results to load
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "result_count"))
        )
        print("Search results loaded successfully")
    except TimeoutException:
        print("Timed out waiting for results to load")
        driver.quit()
        return

    # Create output file if it doesn't exist or append to existing file
    output_file = "coronavirus_data.txt"
    if not os.path.exists(output_file):
        with open(output_file, 'w', encoding='utf-8') as f:
            # Create empty file if it doesn't exist
            pass

    # Function to check if an item has been successfully processed
    def is_item_processed(page_num, item_num):
        if not os.path.exists(output_file):
            return False

        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Check if the metadata for this specific item exists in the file
            pattern = rf"{page_num}, {item_num},"
            return re.search(pattern, content) is not None

    # Navigate to the start page
    if start_page > 1:
        try:
            print(f"Navigating to start page {start_page}...")
            # Wait for page navigation elements to be available
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "pageno2"))
            )

            page_input = driver.find_element(By.ID, "pageno2")
            page_input.clear()
            page_input.send_keys(str(start_page))
            page_input.send_keys(Keys.ENTER)

            # Wait for page to load
            time.sleep(3)
            print(f"Successfully navigated to page {start_page}")
        except Exception as e:
            print(f"Error navigating to start page: {e}")
            driver.quit()
            return

    # Process pages
    current_page = start_page

    while current_page <= end_page:
        print(f"Processing page {current_page}...")

        # Wait for results to load completely
        time.sleep(2)

        # Get all result items on the page
        try:
            result_items = driver.find_elements(By.CSS_SELECTOR, "div.rslt")
            print(f"Found {len(result_items)} results on this page")

            for idx, item in enumerate(result_items):
                item_num = idx + 1
                # Check if this item has already been processed
                if is_item_processed(current_page, item_num):
                    print(
                        f"Item {item_num} on page {current_page} already processed. Skipping...")
                    continue

                # Retry loop for each item
                for retry_count in range(max_retries):
                    try:
                        if retry_count > 0:
                            print(
                                f"Retry attempt {retry_count} for item {item_num}")
                            # Refresh the list of items
                            result_items = driver.find_elements(
                                By.CSS_SELECTOR, "div.rslt")
                            if idx < len(result_items):
                                item = result_items[idx]
                            else:
                                print(
                                    f"Item {item_num} not found after page refresh. Skipping...")
                                break

                        # Extract title/name
                        title_element = item.find_element(
                            By.CSS_SELECTOR, "p.title a")
                        title_text = title_element.text.strip()
                        print(
                            f"Processing item {item_num}: {title_text[:50]}...")

                        # Extract description/metadata
                        desc_element = item.find_element(
                            By.CSS_SELECTOR, "p.desc")
                        desc_text = desc_element.text.strip()

                        # Extract protein length
                        # For proteins, we look for amino acids (aa) instead of base pairs (bp)
                        aa_match = re.search(r'([\d,]+)\s+aa', desc_text)
                        aa_length = aa_match.group(1) if aa_match else "Unknown"

                        # Get direct FASTA URL from the title link
                        title_href = title_element.get_attribute("href")
                        if not title_href:
                            print(f"Could not get URL for item {item_num}")
                            continue

                        # Transform to FASTA URL
                        accession_match = re.search(
                            r'/protein/([^?]+)', title_href)
                        if not accession_match:
                            print(
                                f"Could not extract accession number for item {item_num}")
                            continue

                        accession = accession_match.group(1)
                        fasta_url = f"https://www.ncbi.nlm.nih.gov/protein/{accession}?report=fasta"

                        # Open FASTA URL in new tab
                        driver.execute_script(
                            "window.open(arguments[0]);", fasta_url)

                        # Switch to the new tab
                        time.sleep(1)
                        original_window = driver.current_window_handle
                        for window_handle in driver.window_handles:
                            if window_handle != original_window:
                                driver.switch_to.window(window_handle)
                                break

                        # Wait for FASTA content to load
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located(
                                (By.TAG_NAME, "pre"))
                        )

                        # Extract the FASTA content
                        fasta_element = driver.find_element(By.TAG_NAME, "pre")
                        fasta_text = fasta_element.text

                        # Extract only the sequence part (without header)
                        sequence_lines = fasta_text.strip().split('\n')

                        # Get the header (first line) and remove the '>' character
                        header = sequence_lines[0][1:].strip() if sequence_lines[0].startswith(
                            '>') else sequence_lines[0].strip()

                        # Join all the sequence lines (excluding header) into a single continuous string
                        sequence = ''.join(sequence_lines[1:]).replace(' ', '')

                        # Format: "page number, item number, Name, aa length" as metadata
                        metadata = f"{current_page}, {item_num}, {title_text}, {aa_length} aa"

                        # Write data to file in the required format, using append mode
                        with open(output_file, 'a', encoding='utf-8') as f:
                            f.write(f"{metadata}\n")
                            f.write(f"{sequence}\n")
                            f.write("\n")  # Empty line after each entry

                        print(f"Successfully processed item {item_num}")

                        # Close this tab and switch back to results
                        driver.close()
                        driver.switch_to.window(original_window)

                        # If we get here, the item was successfully processed
                        break

                    except Exception as e:
                        print(f"Error processing item {item_num}: {e}")
                        # Try to close any additional tabs and go back to main window
                        try:
                            if len(driver.window_handles) > 1:
                                # If we're not in the original window, switch back
                                if driver.current_window_handle != original_window:
                                    driver.close()
                                    driver.switch_to.window(original_window)
                        except Exception as tab_error:
                            print(f"Error cleaning up tabs: {tab_error}")

                        # If this was the last retry attempt, log it
                        if retry_count == max_retries - 1:
                            print(
                                f"Failed to process item {item_num} after {max_retries} attempts")
                        else:
                            # Wait a moment before retry
                            time.sleep(2)

            # Navigate to next page if not the last page
            if current_page < end_page:
                try:
                    # Find the page input box
                    page_input = driver.find_element(By.ID, "pageno2")

                    # Get the max page number
                    page_text = driver.find_element(
                        By.CSS_SELECTOR, "h3.page").text
                    max_page_match = re.search(r'of (\d+)', page_text)
                    max_page = int(max_page_match.group(1)
                                   ) if max_page_match else 1

                    # Check if requested end_page is greater than max_page
                    if end_page > max_page:
                        end_page = max_page
                        print(
                            f"Adjusted end_page to {max_page} (max available)")

                    if current_page < max_page:
                        # Clear and set new page number
                        page_input.clear()
                        page_input.send_keys(str(current_page + 1))
                        page_input.send_keys(Keys.ENTER)

                        # Wait for next page to load
                        time.sleep(3)
                        print(f"Navigated to page {current_page + 1}")
                    else:
                        print(f"Reached the last page ({max_page})")
                        break
                except Exception as e:
                    print(f"Error navigating to next page: {e}")
                    break

            current_page += 1

        except Exception as e:
            print(f"Error processing page {current_page}: {e}")
            break

    print(f"Scraping completed. Data saved to {output_file}")
    driver.quit()


if __name__ == "__main__":
    # Get user input for page range
    try:
        start_page = int(input("Enter start page number (default 1): ") or 1)
        end_page = int(input("Enter end page number (default 5): ") or 5)
        max_retries = int(
            input("Enter maximum retry attempts per item (default 3): ") or 3)

        if start_page < 1:
            start_page = 1
            print("Start page set to 1 (minimum value)")
        if end_page < start_page:
            end_page = start_page
            print(
                f"End page set to {start_page} (cannot be less than start page)")
    except ValueError:
        print("Invalid input, using default values: pages 1-5 with 3 retries per item")
        start_page, end_page, max_retries = 1, 5, 3

    scrape_ncbi_coronavirus(start_page, end_page,max_retries)