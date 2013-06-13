Release Notes
=============

0.0.5 (Unreleased)
------------------
* Moved source code into /src and all reusable code into its own directory called 'yape'
* Added a 'Manager' class for loading and storing weak references to assets, such as images, fonts, and JSON files
* Renamed Asset and LoadableAsset classes to Component and LoadableComponent to avoid confusion with image, font and other "assets"
* Made Components use the new 'Manager' class so that any references to loaded files are shared and released effortlessly
* Refactored component loading so that Components also validate, and added a 'post_process' phase.
* Added a 'process_fields' step to Component loading, which allows for the declaration of asset fields such as 'image_fields' that are automatically loaded with the associated manager.
* Created a 'GameData' namedtuple to simplify passing any global singletons that are created at initialization time.

0.0.4 (Released 05-08-2013)
---------------------------
* Feature: Added a popup message when the player misses a question and loses their items
* Bugfix: Removed a monster's coordinates from the level when a monster is defeated.
* Simplified graphics rendering code and associated utilities. Created a Camera class to facilitate this.
* Improved the docstrings and reusability of the FSM class.
* Added a config directory for various config files
* Removed import magic that was used with the dispatcher
* Removed unused data in questions and config JSON files

0.0.3 (Released 04-26-2013)
---------------------------
* Initial public release

