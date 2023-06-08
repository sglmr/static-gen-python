# static-gen
This is the static site generator for my website, which in a very short time has experienced an excessive number of transformations transformations. It started out as a Django project, migrated to Pelican, and then I wanted to try making a simple static site generator with as few depenencies as possible for myself. So here we are.

It doesn't need a server, it doesn't have 10+ dependencies, it doesn't have multiple methods of doing the same thing that conflict with eachother in unexpected ways.

It's simply ran with `python build` and currently throws together my site in fractions of a second.

Now run `python sglmr -r -l` to serve the site and autoreload when changes are detected.

## Someday enhancements
- [ ] RSS Feed
- Tests 😱
  - [ ] page counts
  - [ ] post counts
  - [ ] templates: tags & contents & files
  - [ ] markdown transformations
  - [ ] static files
  - [ ] index.html
  - [ ] robots.txt
  - [ ] sitemap.xml
- Look for settings.py cleanup. Should the templates all be picked up in readers.py?