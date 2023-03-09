from playwright.sync_api import sync_playwright
import inquirer

from jobplatforms import Indeed, OtherPlatform



def jobsearch_platform(page):
    choose_jobsearch_platform = [
        inquirer.List('Choice of Platform',
            message="What platform would you like to jobsearch on?",
            choices=[
                ('Indeed', Indeed), 
                ('Other platform', OtherPlatform)
                ],
                carousel=True
            ),]
    answers = inquirer.prompt(choose_jobsearch_platform)
    return answers['Choice of Platform'](page).run()

with sync_playwright() as playwright:
    chromium = playwright.chromium
    browser = chromium.launch(headless=False)
    page = browser.new_page()
    jobsearch_platform(page)
    # JobScraper(playwright).run()
    