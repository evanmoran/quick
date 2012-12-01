                (_)    | |
      __ _ _   _ _  ___| | __
     / _` | | | | |/ __| |/ /
    | (_| | |_| | | (__|   <
     \__, |\__,_|_|\___|_|\_\
        | |
        |_|

    Quick practical knowledge.
      --Evan Moran

### Tenets of Quick

1. Teach your workflow
2. Be brief and insightful
3. Write for smart [noobs](http://en.wikipedia.org/wiki/Noob)
4. Prefer code snippets over paragraphs

### One Line Install

    curl https://raw.github.com/evanmoran/quick/master/install.sh | sh

### Viewing

    quick git                     View the `git` topic
    quick git:config              View `git:config` subtopic

### Listing

    quick --list                  List all topics
    quick --list git              List `git` subtopics

### Updating

    quick --update                Update quick

### Fancy Shorthand

    quick :                       List all topics
    quick git:                    List subtopics of `git`
    quick git+                    Edit or create `git` topic
    quick git:config+             Edit or create `git:config` subtopic

## Usage

    quick [options] topic[:subtopic]

        -h, --help                Output usage information
        -l, --list                List all quick files with topic
        -e, --edit                Edit topic or subtopic
        -w, --web                 Open quick file in website
        -u, --update              Update quick and its topics cache