from jobsearch import JobScraper


class Indeed(JobScraper):

    def __init__(self, page):
        super().__init__(page)
        self.page = page
        self.url = "https://uk.indeed.com/?r=us"

        # page objects
        self.wrapper_dropdown_remote = self.page.locator("div.yosegi-FilterPill-dropdownPillContainer").nth(2)
        self.dropdown_remote = self.wrapper_dropdown_remote.locator("ul[role=menu]").locator("li[role=menuitem]").nth(0)

        self.field_search = self.page.get_by_placeholder("Job title, keywords, or company")
        self.button_search = self.page.get_by_role("button", name="Find jobs")
        self.button_job_title = self.page.locator("a.jcs-JobTitle")
        self.text_job_description = self.page.locator("div#jobDescriptionText")

        self.next_page_button = self.page.locator("a[data-testid='pagination-page-next']")

    def run(self):
        super().run(self.url, self.field_search, self.button_search, self.wrapper_dropdown_remote, self.dropdown_remote)


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
        

class OtherPlatform(JobScraper):
    def __init__(self) -> None:
        pass