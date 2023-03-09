from playwright.sync_api import sync_playwright


class JobScraper:

    def __init__(self, playwright):
        self.chromium = playwright.chromium
        self.browser = self.chromium.launch(headless=False)
        self.page = self.browser.new_page()

        # page objects
        self.google_box = self.page.locator("button.icl-CloseButton")
        self.cookie_accept = self.page.locator("button#onetrust-accept-btn-handler")
        self.sign_up_bait = self.page.get_by_role("button", name="close")

        self.wrapper_dropdown_remote = self.page.locator("div.yosegi-FilterPill-dropdownPillContainer").nth(2)
        self.dropdown_remote = self.wrapper_dropdown_remote.locator("ul[role=menu]").locator("li[role=menuitem]").nth(0)

        self.field_search = self.page.get_by_placeholder("Job title, keywords, or company")
        self.button_search = self.page.get_by_role("button", name="Find jobs")
        self.button_job_title = self.page.locator("a.jcs-JobTitle")
        self.text_job_description = self.page.locator("div#jobDescriptionText")


        # search criteria
        self.title_must_haves = ["QA"]
        # self.title_should_have_one = ["developer", "software", "automation", "tester", "test", "engineer"]
        self.must_not_haves = ["intern"]

    def run(self):

        self.page.goto("https://uk.indeed.com/?r=us")
        self.remove_covering_boxes()
        self.field_search.fill('junior QA tester')
        self.button_search.click()

        self.page.wait_for_load_state(state="networkidle")
        self.wrapper_dropdown_remote.click()
        self.dropdown_remote.click()

        self.remove_covering_boxes()

        self.job_title_scraping()
        print('Scraping complete')
        self.browser.close()

    def remove_covering_boxes(self):
        self.page.wait_for_load_state(state="networkidle")
        if self.google_box.is_visible():
            self.google_box.click()
        if self.cookie_accept.is_visible():
            self.cookie_accept.click()
        if self.sign_up_bait.is_visible():
            self.sign_up_bait.click()

    def job_title_scraping(self):
        self.button_job_title.nth(0).wait_for(state="visible")
        # ^page registers as loaded when all the links aren't present^
        
        print('\nJob_titles of potential relevance:\n')
        for job_title in self.button_job_title.all():
            self.ensure_job_description_visible(job_title=job_title)
            self.remove_covering_boxes()
            for must_have in self.title_must_haves:
                if must_have in job_title.inner_text():
                    print(f'- {job_title.inner_text()}: {self.page.url}\n')
                    self.remove_covering_boxes()
                    self.ensure_job_description_visible(job_title=job_title)

    def ensure_job_description_visible(self, job_title):
        try:
            self.text_job_description.wait_for(state='visible', timeout=5000)
        except:
            while self.text_job_description.is_hidden():
                job_title.click()
                try:
                    self.text_job_description.wait_for(state='visible', timeout=5000)
                except:
                    print(f'Unable to display: {self.text_job_description} by clicking {job_title}.')

with sync_playwright() as playwright:
    JobScraper(playwright).run()