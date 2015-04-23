# eee (Edge edX Export)

Provides an user friendly export tool from edge.edx.com discussion boards,
that allows a user to get a  page showcasing their contributions.

## Goals
* Allow user curation of their material (selecting and ordering posts)
* Include a mechanism for some users's posts to be anonymized or deleted
  in the exports of others.
* The export should be a static HTML page that the user can host anywhere.
* The exported site should be intuitive and visually appealing.


## Example
```
$ http --timeout 360 --form POST https://eee-api.herokuapp.com/ \
  email=sshanabrook@colgate.edu \
  password=<your password> \
  id_number=50081 \
  institution=ColgateX \
  course_num=CORE138 \
  section=2015_SP
```
