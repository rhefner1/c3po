# C-3PO Bot

## Intro

Hello - I am C-3PO, human-cyborg relations!  I was created with the mission of assisting the Beasts of the East with anything and everything that I can. I can respond to events or perform various actions.

I can currently connect to chat rooms hosted on GroupMe, though I have the ability to expand to more places further down the road.

I was lovingly created by [Ryan Hefner](http://r.hefner1.com) and everyone else listed [here](https://github.com/rhefner1/c3po/graphs/contributors).

## Commands
### Base

You can address me as `c3po` or `C-3PO`. There are some commands that I will only respond to if I'm addressed and there are some that I'll respond to no matter what:

| Command                                        | Response                                  |
|:-----------------------------------------------|:------------------------------------------|
| c3po who created you?                          | Tribute to the authors.                   |
| c3po hi/hello                                  | I'll greet you.                           |
| c3po motivate [person]                         | Says something nice about the person.     |
| c3po ping                                      | pong                                      |
| c3po tell [person] to [action]                 | I'll tell someone to do something.        |
| c3po tell [person] that he/she should [action] | Same as above.                            |
| c3po thank you                                 | You're welcome!                           |
| c3po weather                                   | I'll get the latest weather info.         |
| c3po what can you do                           | Directs to a page detailing capabilities. |
| c3po wolf                                      | PACK!                                     |

### Small Groups (includes Base)
| Command                     | Response                                                           |
|:----------------------------|:-------------------------------------------------------------------|
| clark?                      | Checks if Clark Dining Hall is open. If it is, prints the menu.    |

### Beasts of the East (includes Small Groups)
| Command         | Response      |
|:----------------|:--------------|
| babe wait       | Hot Rod quote |
| cool beans      | Hot Rod quote |
| gods of war     | Hot Rod quote |
| legit           | Hot Rod quote |
| i like to party | Hot Rod quote |
| safe word       | Hot Rod quote |

### Best Eastside Study (includes Small Groups)
| Command | Response |
|:--------|:---------|
|         |          |

### Sara Lane
| Command | Response |
|:--------|:---------|
|         |          |

## Codebase Structure
The C-3PO codebase is laid out as follows:

```
├── app.yaml: Google App Engine routing info
├── c3po: core code files
│   ├── db: data models stored in the database
│   ├── provider: handlers to communicate with a messaging service
│   ├── persona: defines the different 'personas' that C-3PO can
├── ci: scripts used by CI
├── cron.yaml: regularly scheduled cron jobs
├── README.md: the file you're currently reading
└── tests: unit tests
```

Most code contributions will go into `c3po/persona` with tests in `tests/persona` and documentation in `README.md`. Additions to `db` may be necessary if there is a need for persistent data.

## Travis Status
![Travis Build Status](https://api.travis-ci.org/rhefner1/c3po.svg)
