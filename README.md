cs195
=====

Website and public materials for UC Berkeley CS 195

Publishing
----------

* [Install Ruby >= 2.5.0 and Jekyll prerequisites](https://jekyllrb.com/docs/installation/).
  * You'll need an initial version of the `bundler` gem, so run `gem install bundler`.
* Inside `cs195`, run `bundle install`
* Run local server using `bundle exec jekyll serve`
* Notes:
  * As of fa18, you can just edit markdown files directly and push to server and they'll be autodeployed.
  * sp22: upgraded to templar v2
  * sp23: switched to Jekyll

Deploying
----------

* The [publishing workflow](.github/publish-site.yml) runs on Github Actions, and:
  * Builds the site using Jekyll
  * Uses `rsync` to deploy the site to the instructional machines
  * The deploy location is defined by the environment variables. Update `term`
    to push to a new directory on the remote.
