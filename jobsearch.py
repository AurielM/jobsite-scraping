
class JobScraper:

    def __init__(self, page):

        self.page = page

        # page objects
        self.google_box = self.page.locator("button.icl-CloseButton")
        self.cookie_accept = self.page.locator("button#onetrust-accept-btn-handler")
        self.sign_up_bait = self.page.get_by_role("button", name="close")

        self.button_job_title = self.page.locator("a.jcs-JobTitle")
        self.text_job_description = self.page.locator("div#jobDescriptionText")

        self.next_page_button = self.page.locator("a[data-testid='pagination-page-next']")

        # search criteria
        self.title_must_haves = ["QA"]
        # self.title_should_have_one = ["developer", "software", "automation", "tester", "test", "engineer"]
        self.must_not_haves = ["intern", "Night Shift"]

    def run(self, url, field_search, button_search, wrapper_dropdown_remote, dropdown_remote):

        self.page.goto(url)
        self.remove_covering_boxes()
        field_search.fill('QA tester')
        button_search.click()

        self.page.wait_for_load_state(state="networkidle")
        wrapper_dropdown_remote.click()
        dropdown_remote.click()

        self.remove_covering_boxes()

        self.jobs_available = True
        while self.jobs_available:
            self.job_title_scraping()
            self.next_page()
        
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


    def next_page(self):
        try:
            self.next_page_button.wait_for(state='visible', timeout=5000)
            print('Next paging')
            self.next_page_button.click()
        except:
            print("No further pages to search")
            self.jobs_available = False
            return self.jobs_available
