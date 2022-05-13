# A Formal Model of Metacontrol in Maude
## Overview
This repository contains a formal model, written in Maude, of a Smart Home Case Study that uses Metacontrol.

## Download and run
To run the program, Maude needs to be installed. Guidelines for the installation can be found [here](http://maude.cs.illinois.edu/w/index.php/Maude_download_and_installation).

To start Maude and load all files, go to the `additional_modules` directory and run
```
maude test.maude
```
which will not only load the `test.maude` file, but also all other files that are necessary for the execution (the other modules are loaded within the `test.maude` file).

## Test
Once the files are loaded, you can simulate how the controllers work by using the `frew` command. You have to specify how many rewrite steps the system should do, otherwise it will not terminate. The 200 time steps that are displayed in the paper can be simulated by using `frew[1400]`. The `test.maude` file contains initial configurations to test the Comfort-, the Eco-, and the Metacontroller. They can be tested by running
```
frew[1400] initComfort .
frew[1400] initEco .
frew[1400] init initMetacontr .
```
where the first command uses a configuration with only the Comfort controller, the second uses a configuration with only the Eco controller, and the third uses a configuration with the Comfort-, Eco-, Degraded A -, Degraded B -, and Metacontroller.

Other initial configurations with for example a different initial temperature or air quality, can be tested by changing the respective values in `test.maude`.

If you want to see which rules are applied during the rewriting process, run
```
set print attribute on .
```
This can be reverted by running
```
set print attribute off .
```

## Automatic generation of log files and plots
If you also want to create the plots that show the temperature and air quality changes for the Comfort-, Eco-, and Metacontroller, then you have to go to the `test.maude` file and delete `eof`, which can be found at the bottom of the file. The end of the file should now look like this:
```
endm
frew[1400] initComfort .
frew[1400] initEco .
frew[1400] initMetacontr .
quit
```
If Maude is still running, run `quit` to quit it. Otherwise, go to the main folder. By running
```
./run_smart_home.sh
```
the initial configurations with the Comfort-, Eco-, and Metacontroller will be executed for 200 time steps and plots of their performance will be displayed.

If you want to test the system again without plotting the graphs, then insert `eof` again after `endm`, i.e. the end of the `test.maude` file should look like this:
```
endm
eof
frew[1400] initComfort .
frew[1400] initEco .
frew[1400] initMetacontr .
quit
```

## Structure of the modules
![maude_structure](https://user-images.githubusercontent.com/58590193/165742281-a26e551d-13c9-4d05-bea5-389ccb715946.png)
