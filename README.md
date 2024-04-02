# User Guide for VISION
**Version**: V1.0.0

## Contents
- [Introduction](#introduction)
  - [Overview](#overview)
  - [Purpose](#purpose)
  - [Key Features](#key-features)
  - [Target Audience](#target-audience)
- [Getting Started](#getting-started)
  - [System Requirements](#system-requirements)
  - [Note to Users](#note-to-users)
  - [Testing Disclaimer](#testing-disclaimer)
  - [Installation Instructions](#installation-instructions)
    - [Standalone Version Installation](#standalone-version-installation)
      - [Windows](#windows)
      - [macOS](#macOS)
    - [Python-Based Version Setup](#python-based-version-setup)
  - [First Launch](#first-launch)
- [Navigating the Interface](#navigating-the-interface)
- [Setting Panel](#setting-panel)
  - [Load and Table Interaction Section](#load-and-table-interaction-section)
  - [Test, Run, and Analysis Settings](#test-run-and-analysis-settings)
  - [Specific Analysis Settings](#specific-analysis-settings)
    - [Membrane Settings – β Value and Analysis](#membrane-settings--β-value-and-analysis)
    - [Membrane Settings – Global Membrane Masking Options](#membrane-settings--global-membrane-masking-options)
    - [Cytosol Settings](#cytosol-settings)
    - [Advanced Settings](#advanced-settings)
    - [Data Saving](#data-saving)
- [Results Panel](#results-panel)
- [Basic Project Walk Through](#basic-project-walk-through)
- [Youtube Tutorials](#youtube-tutorials)
- [Advanced Features](#advanced-features)
- [Using '*.ome.tiff' as image format](#using-ome-tiff-as-image-format)
- [Troubleshooting and Support](#troubleshooting-and-support)
  - [Reporting Bugs](#reporting-bugs)
- [Appendix](#appendix)
- [License](#license)

## Introduction

### Overview
VISION is a sophisticated software tool specifically designed to analyze and process biological and microscopic images. With its user-friendly interface and powerful backend, it simplifies the complexities involved in image analysis, making it an indispensable resource for researchers, biologists, and educators alike.

### Purpose
The primary aim of VISION is to provide an intuitive yet powerful platform for the analysis of high-resolution image data. Whether it's for academic research, pharmaceutical developments, or educational purposes, VISION streamlines the process of extracting meaningful insights from intricate images, facilitating advancements in scientific understanding and applications.

### Key Features
- **Advanced Image Processing**: Equipped with state-of-the-art algorithms for image enhancement, segmentation, and filtering, ensuring high-quality analysis outputs.
- **Object Detection and Quantification**: Features robust tools for identifying and measuring various characteristics of objects within images, such as area, perimeter, and intensity.
- **Customizable Workflows**: Offers flexibility in analysis procedures, allowing users to adjust parameters and apply different analytical techniques to suit specific research needs.
- **Multi-Dimensional Imaging Support**: Capable of handling 2D, 3D, and time-lapse images, accommodating a wide range of scientific imaging requirements.
- **Comprehensive Data Visualization and Export**: Integrates visualization tools for immediate analysis result review and supports exporting data in multiple formats for further analysis or reporting.
- **Plugin Architecture for Enhanced Functionality**: Allows for the integration of custom plugins, extending the software's capabilities to meet unique analysis demands (Python script only).

VISION stands as a bridge between complex image analysis tasks and actionable scientific insights, embodying a blend of accessibility, precision, and comprehensiveness designed to empower users across various scientific fields.

### Target Audience
The target audience for VISION encompasses a diverse group of individuals and professionals in fields where biological and microscopic image analysis plays a crucial role. The software is designed with features and functionalities that cater to the needs of:

- Researchers and Scientists: Individuals involved in biological, medical, and material science research who require detailed analysis of microscopic images to support their experiments and findings.
- Biologists and Bioinformaticians: Professionals who study cellular structures, functions, and processes, needing advanced tools to quantify and analyze biological data obtained from various imaging techniques.
- Educators and Academics: Teachers and lecturers in universities and colleges who require image analysis software for educational purposes, demonstrating concepts in cell biology, histology, and related fields to students.
- Medical Professionals: Pathologists, clinicians, and other healthcare providers who utilize microscopic imaging for diagnostics, research, and understanding disease mechanisms at the cellular and molecular levels.
- Pharmaceutical and Biotechnology Companies: R&D departments that focus on drug discovery, development, and quality control, where microscopic image analysis is essential for understanding compound effects and ensuring product quality.
- Graduate and Postgraduate Students: Students pursuing advanced degrees in fields such as biology, biomedical engineering, and materials science who need to analyze and interpret image data as part of their thesis or research projects.
- Imaging Specialists and Technologists: Individuals specializing in the operation of microscopic imaging equipment and the analysis of imaging data, looking for robust software to enhance image quality and extract relevant information.

This diverse audience benefits from VISION's ability to process and analyze complex imaging data accurately, making it an invaluable tool for advancingscientific research, education, and professional practice.

## Getting Started

### System Requirements
- **Operating System**: Windows 7 or later, macOS 10.13 (High Sierra) or later, Linux (Ubuntu 16.04 or later, CentOS 7 or later). These are general guidelines; VISION should run on any system where Python is supported.
- **Python Version**: Python 3.6 or newer. It's essential to have a compatible Python version for the software's dependencies.
- **Memory (RAM)**: A minimum of 4 GB RAM, although 8 GB or more is recommended for processing large images or datasets.
- **Processor**: Intel Core i5 or equivalent, with at least 2 GHz processing speed. More advanced processors (i7, i9, or equivalent) can significantly improve performance, especially for computationally intensive tasks.
- **Hard Disk Space**: At least 1.5 GB of free space for installation, with additional space required for storing image data and analysis results.

### Note to Users
These requirements are provided as a general guideline based on typical software dependencies and the performance needs of image analysis tasks. Users with specific or advanced usage scenarios (e.g., handling very large datasets, 3D imaging, time-lapse analyses) might require more powerful hardware. We encourage users to consider their particular needs and consult with their IT department or professionals when setting up systems for VISION. Additionally, future versions of the software or updates to dependencies may alter these requirements.

### Testing Disclaimer
Please note that these system requirements are based on general expectations for software of this nature and have not been rigorously tested across all platforms. Performance can vary based on the specific hardware and software environment, size and complexity of the data being processed, and specific tasks being performed. We welcome feedback from our user community to help refine these recommendations over time.

### Installation Instructions
VISION is designed to be easily accessible, offering both a standalone version for a straightforward installation across Windows, macOS, and Linux, as well as a Python-based version for advanced users or developers. Below are the steps to get started with either version.

#### Standalone Version Installation
**General Steps for All Platforms:**
1. Download the ZIP file for your respective operating system (Windows, macOS, or Linux) from the VISION official website.
2. Extract the ZIP file to your desired location. This will create a folder containing the VISION executable and all necessary dependencies.

##### **Windows:**
- Navigate to the extracted folder and double-click on `VISION.exe` to start the application.

##### **macOS:**
- Open the extracted folder, find the `VISION.app` file, and double-click to launch it. If you encounter any security prompts preventing the app from opening (due to macOS Gatekeeper), right-click (or Control-click) the app and select Open, then confirm in the dialog #

**Quick Guide for Running Blocked Applications on macOS**

macOS prevents certain applications from running due to security restrictions, particularly those downloaded from the internet and not signed by a verified developer.

**Step 1: Grant Execution Permission**

- **Command**: `chmod +x /path/to/VISION(the folder)/VISION(theapp)`
- **Purpose**: Grants execute permission to your application, making it runnable on your system.
- **Usage**: Replace `/path/to/VISION(the folder)/VISION(theapp)` with the actual path to the application you wish to run.

**Step 2: Remove Quarantine Attribute**

- **Command**: `xattr -cr /path/to/VISION(the folder)`
- **Purpose**: Removes the quarantine attribute macOS applies to files downloaded from the internet, which causes the security block.
- **Usage**: Replace `/path/to/VISION(the folder)` with the path to the affected application and folder (_internal) containing multiple blocked files.

**Notes**

- These steps are particularly useful for applications blocked by macOS due to lack of a verified developer signature or for files marked as unsafe because they were downloaded from the internet.
- Always ensure you trust the source of the software you're attempting to run, as bypassing these protections can expose your system to risks.
- This guide is intended to help users quickly resolve issues with running applications that macOS has blocked due to its security settings.


**Linux(Not supported yet):**
- Open a terminal and change to the directory containing the extracted files.
- Make the VISION binary executable with the command: `chmod +x VISION` (replace `VISION` with the actual name of the binary file).
- Run the application by typing `./VISION` in the terminal.

#### Python-Based Version Setup
For those who prefer the flexibility of a Python environment or wish to integrate VISION into their existing workflows, follow these general steps:
1. **Ensure Python is Installed**: VISION requires Python 3.6 or newer. If you don't have Python installed, download it from [https://www.python.org/](https://www.python.org/).
2. **Install Dependencies**: Some Python packages are required to run VISION. Install them using pip by running `pip install -r requirements.txt` in your terminal or command prompt, assuming a `requirements.txt` file is provided with the necessary package names.
3. **Download and Run VISION**: Download the VISION Python scripts and run them in your preferred Python environment or IDE.

**Additional Resources:**
- Python Official Documentation: [https://docs.python.org/3/using/index.html](https://docs.python.org/3/using/index.html)
- pip Documentation: [https://pip.pypa.io/en/stable/user_guide/](https://pip.pypa.io/en/stable/user_guide/)
- IDE Recommendations: Consider using an IDE such as PyCharm, Visual Studio Code, Spyder, or Jupyter Notebooks for a more integrated development experience.

**Note**
The standalone version simplifies the installation process by bundling the application with all its dependencies. It's ideal for users who prefer a quick setup without the need to manually install Python or additional packages. For detailed guides on using Python and managing packages, refer to the provided additional resources.

### First Launch
Welcome to VISION! As you start the application for the first time, here's what you can expect and how to navigate the initial setup process.

**What to Expect:**
- **Console Window**: Upon launching VISION, a console window will appear. This window is an essential part of the application, providing real-time feedback, status updates, and information about the tasks being performed. It's normal for this console to remain open throughout your use of VISION, as it will display valuable information during the application's run.
- **Splash Screen (Windows Only)**: Shortly after the console window opens, you'll be greeted by a splash screen. This splash screen serves as a visual indicator that VISION is in the process of starting up. It's designed to provide a friendly welcome while the application loads the necessary components in the background.
- **Initial Loading Time**: The first startup of VISION may take some time, which is completely normal and depends on your system's specifications. This initial loading allows VISION to properly initialize and prepare for optimal performance. We appreciate your patience during this process.
- **GUI Appearance**: Once initialization is complete, the main graphical user interface (GUI) of VISION will appear. This is where you will interact with the software to load images, perform analyses, and view results. The GUI is designed to be user-friendly and intuitive, providing easy access to all of VISION's powerful features.
- **Console Window During Use**: As mentioned, the console window will remain open while you use VISION. It will continue to provide important messages and updates. Keeping an eye on the console can offer insights into the application's processes and alert you to any actions required on your part.

**Getting Started**: With the GUI open, you are now ready to begin exploring VISION. Whether you're analyzing your first image or configuring settings for your analysis, VISION is equipped to support your work.

**A Note on Performance**: The performance and responsiveness of VISION after the initial launch will vary based on the complexity of the tasks you're performing and your computer's hardware. For demanding tasks or large datasets, enhanced system specifications can contribute to smoother operation.

## Navigating the Interface

Welcome to VISION! This section will help you become familiar with the main window's interface, ensuring you can navigate the software efficiently and make the most out of its powerful features.
![image](https://github.com/biosciflo/VISON/assets/106735259/6072d1b8-ca1c-4484-9741-74ebf34fb299)

### Main Window (1) Overview
The main window of VISION is designed with intuitiveness and efficiency in mind, structured to facilitate easy access to all necessary tools and functionalities for comprehensive image analysis. Here's what you'll find:

- **Settings Panel (2)**: Positioned to maximize ease of access, the Settings Panel is where you'll begin your journey with VISION. From top to bottom, it comprises:
  - **Load and Table Interaction Section**: At the very top, this area allows you to load images into VISION. Following image loading, the section provides functionalities for interacting with the list (table) of loaded images, making it easier to manage and select specific datasets for analysis.
  - **Table for Loaded Images**: Directly below the interaction tools, this table displays all your loaded images. It serves as a central hub for selecting and organizing your analysis queue, providing an overview of your working datasets.
  - **Test Run and Analysis Settings**: Moving down, this segment of the Settings Panel is dedicated to preparing and initiating your image analyses. Here, you can conduct preliminary tests, run analyses, and adjust general settings that apply to the upcoming analysis tasks.
  - **Specific Analysis Settings**: This section is tailored for fine-tuning the analysis parameters, including:
    - **Membrane Settings**: Adjustments specific to analyzing membrane-related features.
    - **Cytosol Settings**: Settings for analyzing cytosolic components.
    - **Advanced Settings**: Additional parameters for users requiring more control and customization of the analysis process.
    - **Savings Settings**: Options for determining how and where your analysis results are saved.
  - **Mini Console**: Located at the bottom of the Settings Panel, the mini console serves as an interactive feedback area. It displays important user messages, warnings, and recommendations, especially useful if a setting is not correctly configured.

- **Results Panel (3)**: This panel is your destination for viewing the outcomes of your analyses. It is organized into three main tabs, each offering a different perspective on your results:
  - **Mask Results**: Displays the results related to image segmentation or masking, providing insights into the specific areas of interest within your images.
  - **Full Image Results**: Offers a holistic view of the analyzed images, highlighting the overall findings and annotations made by the software.
  - **Object Results**: Focuses on the results at the object level, detailing measurements, classifications, and other quantitative data extracted from individual objects identified in your images.

# Setting Panel

## Load and Table Interaction Section

- **Load Files**: Load one or multiple images (*.lsm, *.czi, *.ome.tiff).
- **Load Folder**: Loads all images in folder with compatible file formats (*.lsm, *.czi, *.ome.tiff).
- **Clear Selection**: Clears (unselects a selected item) in image table. 
- **Delete Entry**: Deletes selected item in image table.
- **Clear Table**: Clears (deletes) full image table.

## Test, Run, and Analysis Settings

- **Test Mask**: Runs the thresholding and masking part of the algorithm and returns the results.
- **Run Analysis**: Runs the full Analysis with the selected sub-options.
- **Object Detection**: Enables/disables Object Detection for the full analysis. 
- **Linearization**: Enables/disables object Linearization for the full analysis. (Enabling Object Detection is mandatory)

## Specific Analysis Settings

### Membrane Settings – β Value and Analysis

- **Channel Settings**: Upon loading image files, fields A, B, C, & D automatically populate with existing channel information, such as '488' or numbers '1-9', derived directly from the original file's metadata. When loading spectral LSM or CZI files, the results in the comboboxes will include all available channel wavelengths.
- **Membrane Profiler**: Enables/disables Membrane Profiler. 
- **Colocalization**: Enables/disables an additional, independent colocalization channel. The population of the combobox below follows the same procedure as described in Channel Settings above.
- **Equation**: The "Equation" text field leverages the channel settings A, B, C, and D to calculate the β-Value, for example, the GP-Value using the formula “(A-B)/(A+B)”. Please note, only the variables A, B, C, and D are permitted in this field.

### Membrane Settings – Global Membrane Masking Options

- **Thresholding Options – Specific Channel**: Enable/disable the specific channel Thresholding. Uses combobox next to select the channel dedicated to Thresholding (if disabled: default thresholding is used – Channel with lowest intensity used in equation).
- **Thresholding Options – Thresholding Mode**: Choose between Automatic Otsu Algorithm or Manual. (if Manual, Manual Cutoff Level is enabled).
- **Thresholding Options – Manual Cutoff Level**: Enter an Intensity Value as the Cutoff Level for Thresholding.
- **Thresholding Options – Signal to Noise Ratio**: Enter Signal to Noise Ratio for Thresholding algorithm.
- **Thresholding Options – Background Compensation**: Enable/disable Background Compensation mode for the Thresholding algorithm. When enabled, it allows for the adjustment of Background Mean and Standard Deviation through manual modifications. (as well as through “Probe Raw Image”- Probe Raw Image is in the MASK Results Tab, click on button Probe Raw Image and raise a square area of interest (e.g. Background). Mean, median Standard deviation, min & max will be calculated of this area and shown below, additionally, the mean and standard deviation values will be automatically updated as the "Background Mean" and "Background Std" in the Thresholding options.)
- **Masking Options – Compression**: Enable/disable Compression and Compression Value (float).
- **Masking Options – Remove Object**: Enable/disable Remove Objects and Remove Objects Value (int).
- **Masking Options – Fill Holes**: Enable/disable Fill Holes and Fill Holes Value (float).
- **Masking Options – Gaussian Filter**: Enable/disable Gaussian Filter and Gaussian Filter Value (float).
- **Masking Options – Dilation**: Enable/disable Dilation, Dilation Shape, and X/Y Dimensions of Dilation Shape (int).
- **Binning**: Min/Max/Width of Binning. 

### Cytosol Settings

- All Settings as described for the membrane part, but it is performed on the cytosolic regions. 
- **Cytosolic Measurement**: Enable/disable the analysis of cytosolic regions.

### Advanced Settings

- **Object Segmentation – Skeleton Debranching** 
- **Object Segmentation – tol0**
- **Object Segmentation – tol1**
- **Membrane Profiling – Recentering**: Enable/disable Recentering of Integration Element
- **Membrane Profiling – dim_line**
- **Membrane Profiling – Integrations Element**: Integration Element Shape
- **Membrane Profiling – Integrations Element X/Y-Dimension**: Integration Element XY Dimension
- **Membrane Profiling – β-Value Threshold Auto Cut off** 

### Data Saving

- **Select Saving Path**: Choose a different path to save Results (default: path of image) 
- **Save cropped Membrane**: Save membrane images of individual detected objects.
- **Save cropped Cytosol**: Save cytosolic imagesof individual detected objects.
- **Save Linearized Cytosol**: Save linearized images of individual detected objects.
- **Save Phasors**: Save Phasor plots in excel.
- **Save Settings in JSON**: Save used settings in a dedicated JSON File.
- **Save Results in JSON**: Save used settings and all results in a dedicated JSON File.

# Results Panel

Each panel has a Membrane and Cytosolic part and is split into Mask, Full Image, & Object Results Panel.

# Basic Project Walk Through

1. **Start VISON**
2. **Load File(s) / Load Folder**
3. **Inspect RawImage** Inspect all channels and dimensions of your RawImage by clicking onto the Filename in the image table.
4. **(Membrane Settings)** (Optional) Enter Equation for β-Value calculation.
5. **(Membrane Settings)** Select Channels for each used variable in Equation.
6. **(Membrane Settings)** (Optional) Enable and Choose Specific Thresholding Channel.
7. **Test Mask** (if Mask is not optimal follow with Steps a-c, otherwise go to 7)
   a. Move displayed Raw Image (Right Panel of Mask Results) to the channel of Choose Specific Thresholding Channel or used Channel of Equation with the lowest intensity. Click on “Probe Raw Image” and select a background area.
   b. Activate Background Compensation.
   c. Test Mask (if Mask is not optimal follow with Steps d-, otherwise go to 7)
   d. Enable options such as the Gauss Filter, Dilation, Compression, and Fill Holes, then fine-tune their respective parameters until the mask is satisfactory. Proceed to Step 7 upon completion.
8. **Run Analysis – (Full Image)**
   a. Check Full Image Results.
9. **Activate Object Detection**
10. **Run Analysis – (Full Image & Object Detection)**
   a. If an error appears in the mini console, try to adapt the Masking options; it could be that the subroutines can't detect single objects.
   b. Check Full Image Results and Object-Related Results.
   
**Note**: Once you have run the image, all Results are automatically Saved.
## Youtube Tutorials (cooming soon):
- [TUTORIAL1](https://)
- [TUTORIAL2](https://)
- [TUTORIAL3](https://)

# Advanced Features

- **Custom Analyses**: (cooming soon)
- **Patch Processing**: If multiple images are in the Image – List, either:
  - Select Multiple Images and press Run – Selected Images will be Processed.
  Or…
  - Press “Clear Selection” and Press Run - All Images in list will be Processed.
- **Detailed Masking Options**: VISION provides flexible thresholding and masking capabilities. Each masking option available in the global settings is also accessible for individual customization within the "Detailed Masking Options" table (available for membrane and cytosolic part). This level of detail ensures that each slice can be analyzed with precision, accommodating both 3D stacks and time-lapse sequences. Here's how you can customize these settings:
  - Time-Lapse Sequences: For datasets organized by time, the "Detailed Masking Options" table expands dynamically, adding a column for each time point. This feature allows for the adjustment of masking settings uniquely for each time point.
  - 3D Stacks: For spatial (z) slices within a 3D stack, use the dedicated combobox to select the specific time point (T Position) you wish to customize. This selection enables targeted modification of the masking options for individual z-layers.
  - Important Note for Batch Processing:
To apply specific masking options across multiple images in batch processing, it is essential to first initialize the detailed masking settings for each image file listed in the image table. This involves clicking on each file to activate the detailed options. Failing to perform this step may result in a key value error displayed in the mini console. We are aware of this issue and plan to streamline the process in future updates of VISION.


# Using '*.ome.tiff' as imageformat:
Currently image file types of '*.lsm' and '*.czi' can be openend but with '*.ome.tiff' (imagej/fiji) all images can be anlaysed with VISION. 
- Other image types: If you have special image types such as .lif or .obf. Please get in touch with us. We will be happy to implement the image type if you can provide us with some test images. 

## Step by Step guid to get the right '*.ome.tiff' via FIJI/ImageJ.
- (1) First open FIJI/ImageJ
- (2) Load image file as Hyperstack
- (3) Select "Save" as "OME-TIFF..." 
- (4) Enter Filename with the ending '*.ome.tif' (e.g. test.ome.tif)
- (5) Choose Filetype OME-TIFF
- (6) Press save
- (7) if Window with multiple options for T,Z and Channesl appear do not select anything, just press OK.
- (8) Deselect ROIs, Use "Uncompressed" and press OK
- ADD: This can be done with all kind of images supported by VISION or not. e.g LIF files are currently not supported with an export as '*.ome.tif' you export Sinle Sceens form a LIF project.

- **Glossary**: Definitions of terms and concepts used within the guide and software.

# Troubleshooting and Support

- **Common Issues and Solutions**: As of now, no common issues have been identified. However, we acknowledge that problems we have not yet tested may arise. We appreciate your understanding and patience in these matters. We also encourage you to assist us by reporting any problems you encounter. Your feedback is invaluable in helping us continuously improve the software.
- **Software Updates**: We will release eventually, updates where we cover all the bugs which we and you encounter. New releases you will find here at the GitHub repository.
## Reporting Bugs
If you encounter any issues while using our software, we highly encourage you to report them so we can work on fixing them promptly. Here's how to report a bug on GitHub:

Visit the GitHub Repository: Navigate to our software's GitHub repository. If you're not already signed in, GitHub will prompt you to log in or create a new account.

Check Existing Issues: Before submitting a new bug report, please take a moment to check if the issue has already been reported. You can use the repository's search tool to find issues by keywords. If you find an existing issue that matches yours, you can add any new information you have to that issue rather than creating a new one.

Create a New Issue: If your issue is new, click the 'Issues' tab in the repository, and then click the 'New issue' button. If the repository uses issue templates, select the one that matches your situation or choose 'Open a blank issue' if none of the templates fit.

Fill Out the Issue Template: Provide a clear and concise title for your issue. Fill in the template with as much detail as possible. Be sure to include:

- A brief description of the issue.
- Steps to reproduce the issue.
- Expected behavior and what actually happens.
- Any relevant error messages or screenshots. For that please add the "global_error_log.txt" and/or "error_log.txt". They are in the folder were your executable file is located. 
- Your operating system and version, as well as the software version you're using.
- Any files that you used. 
- Submit the Issue: Once you've filled out the template, submit your issue by clicking the 'Submit new issue' button.

Monitor Your Issue: After submitting, keep an eye on your issue for any comments or questions from the development team. They may need more information or provide a workaround or solution.

Your reports play a crucial role in improving the quality of the software, and we appreciate your contributions to making our project better for everyone.

# Appendix

- **FAQs**: Answers to frequently asked questions about the software.

## License

```
                    GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

                            Preamble

  The GNU General Public License is a free, copyleft license for
software and other kinds of works.

  The licenses for most software and other practical works are designed
to take away your freedom to share and change the works.  By contrast,
the GNU General Public License is intended to guarantee your freedom to
share and change all versions of a program--to make sure it remains free
software for all its users.  We, the Free Software Foundation, use the
GNU General Public License for most of our software; it applies also to
any other work released this way by its authors.  You can apply it to
your programs, too.

  When we speak of free software, we are referring to freedom, not
price.  Our General Public Licenses are designed to make sure that you
have the freedom to distribute copies of free software (and charge for
them if you wish), that you receive source code or can get it if you
want it, that you can change the software or use pieces of it in new
free programs, and that you know you can do these things.

  To protect your rights, we need to prevent others from denying you
these rights or asking you to surrender the rights.  Therefore, you have
certain responsibilities if you distribute copies of the software, or if
you modify it: responsibilities to respect the freedom of others.

  For example, if you distribute copies of such a program, whether
gratis or for a fee, you must pass on to the recipients the same
freedoms that you received.  You must make sure that they, too, receive
or can get the source code.  And you must show them these terms so they
know their rights.

  Developers that use the GNU GPL protect your rights with two steps:
(1) assert copyright on the software, and (2) offer you this License
giving you legal permission to copy, distribute and/or modify it.

  For the developers' and authors' protection, the GPL clearly explains
that there is no warranty for this free software.  For both users' and
authors' sake, the GPL requires that modified versions be marked as
changed, so that their problems will not be attributed erroneously to
authors of previous versions.

  Some devices are designed to deny users access to install or run
modified versions of the software inside them, although the manufacturer
can do so.  This is fundamentally incompatible with the aim of
protecting users' freedom to change the software.  The systematic
pattern of such abuse occurs in the area of products for individuals to
use, which is precisely where it is most unacceptable.  Therefore, we
have designed this version of the GPL to prohibit the practice for those
products.  If such problems arise substantially in other domains, we
stand ready to extend this provision to those domains in future versions
of the GPL, as needed to protect the freedom of users.

  Finally, every program is threatened constantly by software patents.
States should not allow patents to restrict development and use of
software on general-purpose computers, but in those that do, we wish to
avoid the special danger that patents applied to a free program could
make it effectively proprietary.  To prevent this, the GPL assures that
patents cannot be used to render the program non-free.

  The precise terms and conditions for copying, distribution and
modification follow.

                       TERMS AND CONDITIONS

  0. Definitions.

  "This License" refers to version 3 of the GNU General Public License.

  "Copyright" also means copyright-like laws that apply to other kinds of
works, such as semiconductor masks.

  "The Program" refers to any copyrightable work licensed under this
License.  Each licensee is addressed as "you".  "Licensees" and
"recipients" may be individuals or organizations.

  To "modify" a work means to copy from or adapt all or part of the work
in a fashion requiring copyright permission, other than the making of an
exact copy.  The resulting work is called a "modified version" of the
earlier work or a work "based on" the earlier work.

  A "covered work" means either the unmodified Program or a work based
on the Program.

  To "propagate" a work means to do anything with it that, without
permission, would make you directly or secondarily liable for
infringement under applicable copyright law, except executing it on a
computer or modifying a private copy.  Propagation includes copying,
distribution (with or without modification), making available to the
public, and in some countries other activities as well.

  To "convey" a work means any kind of propagation that enables other
parties to make or receive copies.  Mere interaction with a user through
a computer network, with no transfer of a copy, is not conveying.

  An interactive user interface displays "Appropriate Legal Notices"
to the extent that it includes a convenient and prominently visible
feature that (1) displays an appropriate copyright notice, and (2)
tells the user that there is no warranty for the work (except to the
extent that warranties are provided), that licensees may convey the
work under this License, and how to view a copy of this License.  If
the interface presents a list of user commands or options, such as a
menu, a prominent item in the list meets this criterion.

  1. Source Code.

  The "source code" for a work means the preferred form of the work
for making modifications to it.  "Object code" means any non-source
form of a work.

  A "Standard Interface" means an interface that either is an official
standard defined by a recognized standards body, or, in the case of
interfaces specified for a particular programming language, one that
is widely used among developers working in that language.

  The "System Libraries" of an executable work include anything, other
than the work as a whole, that (a) is included in the normal form of
packaging a Major Component, but which is not part of that Major
Component, and (b) serves only to enable use of the work with that
Major Component, or to implement a Standard Interface for which an
implementation is available to the public in source code form.  A
"Major Component", in this context, means a major essential component
(kernel, window system, and so on) of the specific operating system
(if any) on which the executable work runs, or a compiler used to
produce the work, or an object code interpreter used to run it.

  The "Corresponding Source" for a work in object code form means all
the source code needed to generate, install, and (for an executable
work) run the object code and to modify the work, including scripts to
control those activities.  However, it does not include the work's
System Libraries, or general-purpose tools or generally available free
programs which are used unmodified in performing those activities but
which are not part of the work.  For example, Corresponding Source
includes interface definition files associated with source files for
the work, and the source code for shared libraries and dynamically
linked subprograms that the work is specifically designed to require,
such as by intimate data communication or control flow between those
subprograms and other parts of the work.

  The Corresponding Source need not include anything that users
can regenerate automatically from other parts of the Corresponding
Source.

  The Corresponding Source for a work in source code form is that
same work.

  2. Basic Permissions.

  All rights granted under this License are granted for the term of
copyright on the Program, and are irrevocable provided the stated
conditions are met.  This License explicitly affirms your unlimited
permission to run the unmodified Program.  The output from running a
covered work is covered by this License only if the output, given its
content, constitutes a covered work.  This License acknowledges your
rights of fair use or other equivalent, as provided by copyright law.

  You may make, run and propagate covered works that you do not
convey, without conditions so long as your license otherwise remains
in force.  You may convey covered works to others for the sole purpose
of having them make modifications exclusively for you, or provide you
with facilities for running those works, provided that you comply with
the terms of this License in conveying all material for which you do
not control copyright.  Those thus making or running the covered works
for you must do so exclusively on your behalf, under your direction
and control, on terms that prohibit them from making any copies of
your copyrighted material outside their relationship with you.

  Conveying under any other circumstances is permitted solely under
the conditions stated below.  Sublicensing is not allowed; section 10
makes it unnecessary.

  3. Protecting Users' Legal Rights From Anti-Circumvention Law.

  No covered work shall be deemed part of an effective technological
measure under any applicable law fulfilling obligations under article
11 of the WIPO copyright treaty adopted on 20 December 1996, or
similar laws prohibiting or restricting circumvention of such
measures.

  When you convey a covered work, you waive any legal power to forbid
circumvention of technological measures to the extent such circumvention
is effected by exercising rights under this License with respect to
the covered work, and you disclaim any intention to limit operation or
modification of the work as a means of enforcing, against the work's
users, your or third parties' legal rights to forbid circumvention of
technological measures.

  4. Conveying Verbatim Copies.

  You may convey verbatim copies of the Program's source code as you
receive it, in any medium, provided that you conspicuously and
appropriately publish on each copy an appropriate copyright notice;
keep intact all notices stating that this License and any
non-permissive terms added in accord with section 7 apply to the code;
keep intact all notices of the absence of any warranty; and give all
recipients a copy of this License along with the Program.

  You may charge any price or no price for each copy that you convey,
and you may offer support or warranty protection for a fee.

  5. Conveying Modified Source Versions.

  You may convey a work based on the Program, or the modifications to
produce it from the Program, in the form of source code under the
terms of section 4, provided that you also meet all of these conditions:

    a) The work must carry prominent notices stating that you modified
    it, and giving a relevant date.

    b) The work must carry prominent notices stating that it is
    released under this License and any conditions added under section
    7.  This requirement modifies the requirement in section 4 to
    "keep intact all notices".

    c) You must license the entire work, as a whole, under this
    License to anyone who comes into possession of a copy.  This
    License will therefore apply, along with any applicable section 7
    additional terms, to the whole of the work, and all its parts,
    regardless of how they are packaged.  This License gives no
    permission to license the work in any other way, but it does not
    invalidate such permission if you have separately received it.

    d) If the work has interactive user interfaces, each must display
    Appropriate Legal Notices; however, if the Program has interactive
    interfaces that do not display Appropriate Legal Notices, your
    work need not make them do so.

  A compilation of a covered work with other separate and independent
works, which are not by their nature extensions of the covered work,
and which are not combined with it such as to form a larger program,
in or on a volume of a storage or distribution medium, is called an
"aggregate" if the compilation and its resulting copyright are not
used to limit the access or legal rights of the compilation's users
beyond what the individual works permit.  Inclusion of a covered work
in an aggregate does not cause this License to apply to the other
parts of the aggregate.

  6. Conveying Non-Source Forms.

  You may convey a covered work in object code form under the terms
of sections 4 and 5, provided that you also convey the
machine-readable Corresponding Source under the terms of this License,
in one of these ways:

    a) Convey the object code in, or embodied in, a physical product
    (including a physical distribution medium), accompanied by the
    Corresponding Source fixed on a durable physical medium
    customarily used for software interchange.

    b) Convey the object code in, or embodied in, a physical product
    (including a physical distribution medium), accompanied by a
    written offer, valid for at least three years and valid for as
    long as you offer spare parts or customer support for that product
    model, to give anyone who possesses the object code either (1) a
    copy of the Corresponding Source for all the software in the
    product that is covered by this License, on a durable physical
    medium customarily used for software interchange, for a price no
    more than your reasonable cost of physically performing this
    conveying of source, or (2) access to copy the
    Corresponding Source from a network server at no charge.

    c) Convey individual copies of the object code with a copy of the
    written offer to provide the Corresponding Source.  This
    alternative is allowed only occasionally and noncommercially, and
    only if you received the object code with such an offer, in accord
    with subsection 6b.

    d) Convey the object code by offering access from a designated
    place (gratis or for a charge), and offer equivalent access to the
    Corresponding Source in the same way through the same place at no
    further charge.  You need not require recipients to copy the
    Corresponding Source along with the object code.  If the place to
    copy the object code is a network server, the Corresponding Source
    may be on a different server (operated by you or a third party)
    that supports equivalent copying facilities, provided you maintain
    clear directions next to the object code saying where to find the
    Corresponding Source.  Regardless of what server hosts the
    Corresponding Source, you remain obligated to ensure that it is
    available for as long as needed to satisfy these requirements.

    e) Convey the object code using peer-to-peer transmission, provided
    you inform other peers where the object code and Corresponding
    Source of the work are being offered to the general public at no
    charge under subsection 6d.

  A separable portion of the object code, whose source code is excluded
from the Corresponding Source as a System Library, need not be
included in conveying the object code work.

  A "User Product" is either (1) a "consumer product", which means any
tangible personal property which is normally used for personal, family,
or household purposes, or (2) anything designed or sold for incorporation
into a dwelling.  In determining whether a product is a consumer product,
doubtful cases shall be resolved in favor of coverage.  For a particular
product received by a particular user, "normally used" refers to a
typical or common use of that class of product, regardless of the status
of the particular user or of the way in which the particular user
actually uses, or expects or is expected to use, the product.  A product
is a consumer product regardless of whether the product has substantial
commercial, industrial or non-consumer uses, unless such uses represent
the only significant mode of use of the product.

  "Installation Information" for a User Product means any methods,
procedures, authorization keys, or other information required to install
and execute modified versions of a covered work in that User Product from
a modified version of its Corresponding Source.  The information must
suffice to ensure that the continued functioning of the modified object
code is in no case prevented or interfered with solely because
modification has been made.

  If you convey an object code work under this section in, or with, or
specifically for use in, a User Product, and the conveying occurs as
part of a transaction in which the right of possession and use of the
User Product is transferred to the recipient in perpetuity or for a
fixed term (regardless of how the transaction is characterized), the
Corresponding Source conveyed under this section must be accompanied
by the Installation Information.  But this requirement does not apply
if neither you nor any third party retains the ability to install
modified object code on the User Product (for example, the work has
been installed in ROM).

  The requirement to provide Installation Information does not include a
requirement to continue to provide support service, warranty, or updates
for a work that has been modified or installed by the recipient, or for
the User Product in which it has been modified or installed.  Access to a
network may be denied when the modification itself materially and
adversely affects the operation of the network or violates the rules and
protocols for communication across the network.

  Corresponding Source conveyed, and Installation Information provided,
in accord with this section must be in a format that is publicly
documented (and with an implementation available to the public in
source code form), and must require no special password or key for
unpacking, reading or copying.

  7. Additional Terms.

  "Additional permissions" are terms that supplement the terms of this
License by making exceptions from one or more of its conditions.
Additional permissions that are applicable to the entire Program shall
be treated as though they were included in this License, to the extent
that they are valid under applicable law.  If additional permissions
apply only to part of the Program, that part may be used separately
under those permissions, but the entire Program remains governed by
this License without regard to the additional permissions.

  When you convey a copy of a covered work, you may at your option
remove any additional permissions from that copy, or from any part of
it.  (Additional permissions may be written to require their own
removal in certain cases when you modify the work.)  You may place
additional permissions on material, added by you to a covered work,
for which you have or can give appropriate copyright permission.

  Notwithstanding any other provision of this License, for material you
add to a covered work, you may (if authorized by the copyright holders of
that material) supplement the terms of this License with terms:

    a) Disclaiming warranty or limiting liability differently from the
    terms of sections 15 and 16 of this License; or

    b) Requiring preservation of specified reasonable legal notices or
    author attributions in that material or in the Appropriate Legal
    Notices displayed by works containing it; or

    c) Prohibiting misrepresentation of the origin of that material, or
    requiring that modified versions of such material be marked in
    reasonable ways as different from the original version; or

    d) Limiting the use for publicity purposes of names of licensors or
    authors of the material; or

    e) Declining to grant rights under trademark law for use of some
    trade names, trademarks, or service marks; or

    f) Requiring indemnification of licensors and authors of that
    material by anyone who conveys the material (or modified versions of
    it) with contractual assumptions of liability to the recipient, for
    any liability that these contractual assumptions directly impose on
    those licensors and authors.

  All other non-permissive additional terms are considered "further
restrictions" within the meaning of section 10.  If the Program as you
received it, or any part of it, contains a notice stating that it is
governed by this License along with a term that is a further
restriction, you may remove that term.  If a license document contains
a further restriction but permits relicensing or conveying under this
License, you may add to a covered work material governed by the terms
of that license document, provided that the further restriction does
not survive such relicensing or conveying.

  If you add terms to a covered work in accord with this section, you
must place, in the relevant source files, a statement of the
additional terms that apply to those files, or a notice indicating
where to find the applicable terms.

  Additional terms, permissive or non-permissive, may be stated in the
form of a separately written license, or stated as exceptions;
the above requirements apply either way.

  8. Termination.

  You may not propagate or modify a covered work except as expressly
provided under this License.  Any attempt otherwise to propagate or
modify it is void, and will automatically terminate your rights under
this License (including any patent licenses granted under the third
paragraph of section 11).

  However, if you cease all violation of this License, then your
license from a particular copyright holder is reinstated (a)
provisionally, unless and until the copyright holder explicitly and
finally terminates your license, and (b) permanently, if the copyright
holder fails to notify you of the violation by some reasonable means
prior to 60 days after the cessation.

  Moreover, your license from a particular copyright holder is
reinstated permanently if the copyright holder notifies you of the
violation by some reasonable means, this is the first time you have
received notice of violation of this License (for any work) from that
copyright holder, and you cure the violation prior to 30 days after
your receipt of the notice.

  Termination of your rights under this section does not terminate the
licenses of parties who have received copies or rights from you under
this License.  If your rights have been terminated and not permanently
reinstated, you do not qualify to receive new licenses for the same
material under section 10.

  9. Acceptance Not Required for Having Copies.

  You are not required to accept this License in order to receive or
run a copy of the Program.  Ancillary propagation of a covered work
occurring solely as a consequence of using peer-to-peer transmission
to receive a copy likewise does not require acceptance.  However,
nothing other than this License grants you permission to propagate or
modify any covered work.  These actions infringe copyright if you do
not accept this License.  Therefore, by modifying or propagating a
covered work, you indicate your acceptance of this License to do so.

  10. Automatic Licensing of Downstream Recipients.

  Each time you convey a covered work, the recipient automatically
receives a license from the original licensors, to run, modify and
propagate that work, subject to this License.  You are not responsible
for enforcing compliance by third parties with this License.

  An "entity transaction" is a transaction transferring control of an
organization, or substantially all assets of one, or subdividing an
organization, or merging organizations.  If propagation of a covered
work results from an entity transaction, each party to that
transaction who receives a copy of the work also receives whatever
licenses to the work the party's predecessor in interest had or could
give under the previous paragraph, plus a right to possession of the
Corresponding Source of the work from the predecessor in interest, if
the predecessor has it or can get it with reasonable efforts.

  You may not impose any further restrictions on the exercise of the
rights granted or affirmed under this License.  For example, you may
not impose a license fee, royalty, or other charge for exercise of
rights granted under this License, and you may not initiate litigation
(including a cross-claim or counterclaim in a lawsuit) alleging that
any patent claim is infringed by making, using, selling, offering for
sale, or importing the Program or any portion of it.

  11. Patents.

  A "contributor" is a copyright holder who authorizes use under this
License of the Program or a work on which the Program is based.  The
work thus licensed is called the contributor's "contributor version".

  A contributor's "essential patent claims" are all patent claims
owned or controlled by the contributor, whether already acquired or
hereafter acquired, that would be infringed by some manner, permitted
by this License, of making, using, or selling its contributor version,
but do not include claims that would be infringed only as a
consequence of further modification of the contributor version.  For
purposes of this definition, "control" includes the right to grant
patent sublicenses in a manner consistent with the requirements of
this License.

  Each contributor grants you a non-exclusive, worldwide, royalty-free
patent license under the contributor's essential patent claims, to
make, use, sell, offer for sale, import and otherwise run, modify and
propagate the contents of its contributor version.

  In the following three paragraphs, a "patent license" is any express
agreement or commitment, however denominated, not to enforce a patent
(such as an express permission to practice a patent or covenant not to
sue for patent infringement).  To "grant" such a patent license to a
party means to make such an agreement or commitment not to enforce a
patent against the party.

  If you convey a covered work, knowingly relying on a patent license,
and the Corresponding Source of the work is not available for anyone
to copy, free of charge and under the terms of this License, through a
publicly available network server or other readily accessible means,
then you must either (1) cause the Corresponding Source to be so
available, or (2) arrange to deprive yourself of the benefit of the
patent license for this particular work, or (3) arrange, in a manner
consistent with the requirements of this License, to extend the patent
license to downstream recipients.  "Knowingly relying" means you have
actual knowledge that, but for the patent license, your conveying the
covered work in a country, or your recipient's use of the covered work
in a country, would infringe one or more identifiable patents in that
country that you have reason to believe are valid.

  If, pursuant to or in connection with a single transaction or
arrangement, you convey, or propagate by procuring conveyance of, a
covered work, and grant a patent license to some of the parties
receiving the covered work authorizing them to use, propagate, modify
or convey a specific copy of the covered work, then the patent license
you grant is automatically extended to all recipients of the covered
work and works based on it.

  A patent license is "discriminatory" if it does not include within
the scope of its coverage, prohibits the exercise of, or is
conditioned on the non-exercise of one or more of the rights that are
specifically granted under this License.  You may not convey a covered
work if you are a party to an arrangement with a third party that is
in the business of distributing software, under which you make payment
to the third party based on the extent of your activity of conveying
the work, and under which the third party grants, to any of the
parties who would receive the covered work from you, a discriminatory
patent license (a) in connection with copies of the covered work
conveyed by you (or copies made from those copies), or (b) primarily
for and in connection with specific products or compilations that
contain the covered work, unless you entered into that arrangement,
or that patent license was granted, prior to 28 March 2007.

  Nothing in this License shall be construed as excluding or limiting
any implied license or other defenses to infringement that may
otherwise be available to you under applicable patent law.

  12. No Surrender of Others' Freedom.

  If conditions are imposed on you (whether by court order, agreement or
otherwise) that contradict the conditions of this License, they do not
excuse you from the conditions of this License.  If you cannot convey a
covered work so as to satisfy simultaneously your obligations under this
License and any other pertinent obligations, then as a consequence you may
not convey it at all.  For example, if you agree to terms that obligate you
to collect a royalty for further conveying from those to whom you convey
the Program, the only way you could satisfy both those terms and this
License would be to refrain entirely from conveying the Program.

  13. Use with the GNU Affero General Public License.

  Notwithstanding any other provision of this License, you have
permission to link or combine any covered work with a work licensed
under version 3 of the GNU Affero General Public License into a single
combined work, and to convey the resulting work.  The terms of this
License will continue to apply to the part which is the covered work,
but the special requirements of the GNU Affero General Public License,
section 13, concerning interaction through a network will apply to the
combination as such.

  14. Revised Versions of this License.

  The Free Software Foundation may publish revised and/or new versions of
the GNU General Public License from time to time.  Such new versions will
be similar in spirit to the present version, but may differ in detail to
address new problems or concerns.

  Each version is given a distinguishing version number.  If the
Program specifies that a certain numbered version of the GNU General
Public License "or any later version" applies to it, you have the
option of following the terms and conditions either of that numbered
version or of any later version published by the Free Software
Foundation.  If the Program does not specify a version number of the
GNU General Public License, you may choose any version ever published
by the Free Software Foundation.

  If the Program specifies that a proxy can decide which future
versions of the GNU General Public License can be used, that proxy's
public statement of acceptance of a version permanently authorizes you
to choose that version for the Program.

  Later license versions may give you additional or different
permissions.  However, no additional obligations are imposed on any
author or copyright holder as a result of your choosing to follow a
later version.

  15. Disclaimer of Warranty.

  THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY
APPLICABLE LAW.  EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT
HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY
OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE.  THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM
IS WITH YOU.  SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF
ALL NECESSARY SERVICING, REPAIR OR CORRECTION.

  16. Limitation of Liability.

  IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING
WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR CONVEYS
THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY
GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE
USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF
DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD
PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS),
EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF
SUCH DAMAGES.

  17. Interpretation of Sections 15 and 16.

  If the disclaimer of warranty and limitation of liability provided
above cannot be given local legal effect according to their terms,
reviewing courts shall apply local law that most closely approximates
an absolute waiver of all civil liability in connection with the
Program, unless a warranty or assumption of liability accompanies a
copy of the Program in return for a fee.

                     END OF TERMS AND CONDITIONS

            How to Apply These Terms to Your New Programs

  If you develop a new program, and you want it to be of the greatest
possible use to the public, the best way to achieve this is to make it
free software which everyone can redistribute and change under these terms.

  To do so, attach the following notices to the program.  It is safest
to attach them to the start of each source file to most effectively
state the exclusion of warranty; and each file should have at least
the "copyright" line and a pointer to where the full notice is found.

    <one line to give the program's name and a brief idea of what it does.>
    Copyright (C) <year>  <name of author>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

Also add information on how to contact you by electronic and paper mail.

  If the program does terminal interaction, make it output a short
notice like this when it starts in an interactive mode:

    <program>  Copyright (C) <year>  <name of author>
    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
    This is free software, and you are welcome to redistribute it
    under certain conditions; type `show c' for details.

The hypothetical commands `show w' and `show c' should show the appropriate
parts of the General Public License.  Of course, your program's commands
might be different; for a GUI interface, you would use an "about box".

  You should also get your employer (if you work as a programmer) or school,
if any, to sign a "copyright disclaimer" for the program, if necessary.
For more information on this, and how to apply and follow the GNU GPL, see
<https://www.gnu.org/licenses/>.

  The GNU General Public License does not permit incorporating your program
into proprietary programs.  If your program is a subroutine library, you
may consider it more useful to permit linking proprietary applications with
the library.  If this is what you want to do, use the GNU Lesser General
Public License instead of this License.  But first, please read
<https://www.gnu.org/licenses/why-not-lgpl.html>.
```

