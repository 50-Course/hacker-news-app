# HN News App 👽

Backend API for Hacker News. Written in Django, for `QuickCheck` Backend Software Engineer Position.



## Description




## Documentation

link to dev doc (API doc, Feature lists, system_design, and all): Check the `docs` directory
link to dev blog: {null}

## Dev's Corner

There are so many uncompleted implementations in this codebase,
They are:

- [ ] Migration of my log files to Third party monitoring service e.g Prometheus, my Sentry free-trial license is expried.

- [ ] Elasticsearch using `elasticsearch_dsl` to be configured at later date right now, \
I harded coded the search API, you can find that on: `api.lib.lookups` module.

- [ ] The Asynchronous call of saving to be needs improvement 💩. It's residing in the library `api.libs.collector.py`. _Please, please and please don't peep in the `runsync.py` module._

- [ ] There is a stale version of the early hours of development on my private repository. @50-Course, @TODO: Add GitLab CI runner to codebase.

- [ ] Can't setup pytest, heavy refactoring to be done and then setting up Pytest


**Let's get you started?**

* That birds eye view, we've got you covered. Run `build` up the docker container and head to: `0.0.0.0:8000` on your browser.

**NOTES**:

* Most Django Native views are half-implemented due to deadline. However, documented for clarity to be resumed at a later date.

* Docker was configurd for deployment to Amazon EC2, ECS. Later found out the project requires manual submission.

* There are stale code in this codebases, well documented but bad practices, taking them off at a sooner date.

* I am refactoring this codebase to use Django REST Framework and REST Framework only.

* _Above All, I appreciate review, There are many points in here that needs improvement a quick comment would go a long way thank you._

* Time really went against me in this project however I am continously updating this project on a private repository. Make it public on `https://github.com/50-Course/hacker-news-app`, so please shoot me a dm if you want to see the update code with GitLab CI integrated on the repo. For now I am submitting this.


## License

MIT License
