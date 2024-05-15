# Contributing to MagnetSting
If you are interested in contributing to MagnetSting, have a read through the following sections to understand how
you can.

<!-- Branches -->
## Branches
The repository has two branches: `master` and `dev`. The `master` branch holds all the stable code and is updated once a new 
version is released. The `dev` branch on the other hand is updated more often, with all the new changes first being committed 
to `dev`. Once a new version of MagnetSting is ready, it is then merged with `master`. If you are planning on contributing
to MagnetSting, make sure to base your work off of the `dev` branch as it is always more up to date in terms of the latest
changes. 

<!-- Goals -->
## Goals
MagnetSting was created with two main goals in mind: simplfying something that can be complex and time-consuming and relying 
only on Python's standard library. When contributing to the MagnetSting, please try to keep these two goals in mind.

Regarding simplicity, try to keep the front-end simple and user-friendly. For example, creating a new command should be as easy 
as calling a specific method. Of course, there is always some wiggle room, as "try to keep it simple" is not always realistically 
feasible. The back-end (the actual code of MagnetSting) however allows for more freedom and complexity (but not complex to
the point where even HAL-9000 would have trouble understanding what the code is doing :slightly_smiling_face:).

In terms of adding external modules to MagnetSting, it is preferred to stick to using only modules from Python's standard
library. The reason for this is because MagnetSting was created to be as portable and self-reliant as possible, not requiring
any additional dependencies and being able to run on nearly any machine that has the Python interpreter on it.

<!-- Bugs and Errors -->
## Bugs and Errors
Bugs? Errors? I have no idea what you're talking about :wink:. If you have come across a bug or an error and would like to
graciously help get rid of it, or if you are not sure how to go about it, create a post in the "Issues" area with
"BUG" or "ERROR" in the title. Make sure to describe what the bug/error is, what causes it and how it can be triggered.  

<!-- New Features and Improvements -->
## New Features and Improvements
When adding a new feature, please make sure to add docstrings (ex. if you create a new method) and some comments that explain what 
parts of the code is doing. Also, if necessary, please update the `README.md` file as well. This helps to not only understand 
what your code does but also makes it easier to debug and improve on. If you are improving on an already existing part of 
MagnetSting, please make sure to update the docstrings, comments and/or the `README.md` file if necessary. For example, if you made 
a minor change to a print message, then you don't really need to update any documentation. But if you rewrite an entire method, 
please ensure that you add/edit the various forms of documentation as needed. 

If you have an idea that you would like to see in MagnetSting but are unsure of how to implement it, create a post in the 
in the Discussion area under the "Ideas" section. In the post, describe what your idea is, how it might work, etc. 

If you would like to contribute but are unsure of what to contribute, check out the "Issues" area or the "Ideas" section
in the discussion area and see if there are any bugs, errors or ideas that you would like to take on. 

<!-- Code Style -->
## Code Style 
When working on a contribution, please follow the PEP 8 guidelines with one exception: instead of keeping lines of code
79 characters or less and docstrings/comments 72 characters or less, please keep both lines of code and docstrings/comments 
121 characters or less.

<!-- Code Review -->
## Code Review
Please don't worry if a pull request is not merged right away. To ensure compatability, maintainability and above all, that
MagnetSting continues to work as intended, the pull request is just being reviewed to make sure that it meets the requirements
and doesn't have any unintended effects. 

<!-- Questions-->
## Questions
If at any time you have a question, please feel free to create a post in the "Discussions" area under the "Q&A" category. 

