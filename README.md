# AV-Asset-Manager
Django-based asset management for audio/visual use

(Currently in very early development)

This is a project driven by personal/work-related needs and as such is intended to be very specific.  It will most likely not be something useful if more generic asset-management is needed.

## Goals
* Keep track of items in use/inventory such as:
  * Video:
    * Projectors
      * Lamp Information
        * Model
        * Number of lamps
        * Max Hours
        * Current Hours
      * Filter Information
        * Type (cartridge, washable, scrolling, etc)
        * Model (if applicable)
        * Max Hours
        * Current Hours
    * Other items TBD
  * Lighting
    * Moving Lights
      * Lamp Information (similar to projectors)
  * Others TBD
* Item location/status
  * Installation location (if applicable)
  * Loose inventory
  * History of all changes/updates including date/time and person that made the change
* Asset tagging
  * Implement a unique string id for each asset tying it to the ORM
  * Generate a printable tag including QR code of the string id and the plain text of it
  * Be able to read the QR code through the front-end
    * HTML5 camera api?
    * Uploaded image?
  * Alternatively allow direct input of string id

## TODO
Pretty much everything listed above at the moment
