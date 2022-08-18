# A Formal Model of Metacontrol in Maude
## Overview
This repository contains a formal model, written in Maude, of a Smart Home Use Case that uses Metacontrol.

## Download and run
To run the program, Maude needs to be installed. Guidelines for the installation can be found [here](http://maude.cs.illinois.edu/w/index.php/Maude_download_and_installation).

To start Maude and load all files, first go to the `additional_modules` directory:
```
cd maude/additional_modules/
```

Then run:
```
maude test.maude
```

which will not only load the `test.maude` file, but also all other files that are necessary for the execution (the other modules are loaded within the `test.maude` file).

## Test
### Scenario displayed in paper
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

### Scenarios with breaking actuators
To simulate how the controllers work if an actuator breaks, first load the files as described before. Then, edit the `break.maude` file located at the `maude/additional_modules/` folder. There, you can change the time step when the heater breaks in the `if` condition of the rule `HeaterBreaks` and the time step when the water heater breaks in the `if` condition of the rule `WaterheaterBreaks`.

For example, to change the time step when the water heater breaks to 75, you need to change the `2000000` value in the following rule to 75:
```
crl [WaterheaterBreaks] :
  < WH :Waterheater | Status: WHS, Broken: no, A >
  < C :Clock | Timesteps: TS, Time: TI, TempLog: TL, AqLog: AL >
  =>
  < WH :Waterheater | Status: whOff, Broken: yes, A >
  < C :Clock | Timesteps: TS, Time: TI, TempLog: TL, AqLog: AL >
  if TS >= 2000000
  [print "rule: [WaterheaterBreaks]"] .
```

Like this:
```
crl [WaterheaterBreaks] :
  < WH :Waterheater | Status: WHS, Broken: no, A >
  < C :Clock | Timesteps: TS, Time: TI, TempLog: TL, AqLog: AL >
  =>
  < WH :Waterheater | Status: whOff, Broken: yes, A >
  < C :Clock | Timesteps: TS, Time: TI, TempLog: TL, AqLog: AL >
  if TS >= 75
  [print "rule: [WaterheaterBreaks]"] .
```

Note that we assume that only one actuator can be broken at the same time and that broken actuators do not get repaired. Thus, you should only change one of these values. The results displayed in the paper were obtained if the heater, respectively water heater, broke after 75 time steps. Therefore, to reproduce these results, change one of the values to 75 and run the same `frew` commands as above.

### Variability of the environment
To inject variability of the environment, we implemented two different ways the environment changes over time. They can be found in the file `physics.maude` that is located in the folder `maude/smart_home_model/` in the definition of the function `variabilityEnvir`. Here, you can also define your own environment variability.
To use another way the environment changes, go in the `test.maude` file and change the version of the environment to the desired one. Thus, if you want to run experiments with the second way of changing the environment, change `< Environment | Version: 1 >` to `< Environment | Version: 2 >` in all three initial configurations and run the same `frew` commands as above.

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

## Additional documents
The appendices for the paper can be found [here](https://github.com/JulianePa/Maude_Metacontrol/blob/461bde7ca4778d3b33a92848011c3374d0a0eeee/documents/appendix.pdf).

## Acknowledgments
This project has received funding from the European Union’s Horizon 2020 research and innovation programme under the Marie Skłodowska-Curie grant agreement No. 956200.

Pleave visit [our website](https://remaro.eu/) for more info on our project.

![REMARO Logo](https://remaro.eu/wp-content/uploads/2020/09/remaro1-right-1024.png)
