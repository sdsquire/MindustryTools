# Mindustry Tools
## Overview

This small package is designed to serve as a helper to *Mindustry*, a factory/tower defense game made by Anuke.

## Features

### Feature 1: Factory operations

This package comes with all of the materials, factories, and collectors ~~in the game~~ on Seruplo (need to implement more!). These can be combined with different mathematical operations, resulting in Factory Groups. These operations include:
* **Addition (+):** Adding entities combines them into one entity, summing together their inputs and outputs (given in materials / second).

* **Subtraction (-):** Subtracting entities removes the inputs and outputs of the second entity from the first.

* **Multiplication (\*):** This operation is currently only implemented between floats and factories / factory groups. It scales the input and output rates by that amount.

* **Matrix Multiplication (@):** This scales the inputs and outputs of the second factory such that it covers all of the inputs of the first. This is useful when calculating how many of one factory are required to supply another.

* **Division (/):** This returns a float value representing how many of the second factory are required to supply the inputs of the first.

The function `get_upstream()` is also provided, which repeats the `@` until all inputs are accounted for (by default, still allowing natural materials). Further customizations in the documentation.

### Feature 2: To come!
More features may come, if there is interest. The above feature is what was most pressing to me, but recommendations are welcome!

## Installation
To install, clone this repository (`git clone git@github.com:sdsquire/MindustryTools`).

~~You can also install via the Pypi package: `pip install MindustryTools~~ *(Coming soon!)*

## How to contribute
Suggestions and contributions are welcome. Feel free to create your own branch, then send me a pull request.

## Acknowledgements
Obviously, my big acknowledgement goes to Anuke's game **Mindustry**. I've spent many hours on it, and will probably spend many more. Get it on steam!