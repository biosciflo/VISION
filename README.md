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
    - [Python-Based Version Setup](#python-based-version-setup)
  - [First Launch](#first-launch)
- [Navigating the Interface](#navigating-the-interface)
- [Project Setup](#project-setup)
- [Basic Operations](#basic-operations)
- [Advanced Features](#advanced-features)
- [Troubleshooting and Support](#troubleshooting-and-support)
- [Appendix](#appendix)
  - [Glossary](#glossary)
  - [FAQs](#faqs)
- [Index](#index)
  - [Keyword Index](#keyword-index)
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

**Windows:**
- Navigate to the extracted folder and double-click on `VISION.exe` to start the application.

**macOS:**
- Open the extracted folder, find the `VISION.app` file, and double-click to launch it. If you encounter any security prompts preventing the app from opening (due to macOS Gatekeeper), right-click (or Control-click) the app and select Open, then confirm in the dialog #

**Quick Guide for Running Blocked Applications on macOS**

macOS prevents certain applications from running due to security restrictions, particularly those downloaded from the internet and not signed by a verified developer.

** Step 1: Grant Execution Permission**

- **Command**: `chmod +x /path/to/yourApp`
- **Purpose**: Grants execute permission to your application, making it runnable on your system.
- **Usage**: Replace `/path/to/yourApp` with the actual path to the application you wish to run.

** Step 2: Remove Quarantine Attribute**

- **Command**: `xattr -cr /path/to/yourApplication`
- **Purpose**: Removes the quarantine attribute macOS applies to files downloaded from the internet, which causes the security block.
- **Usage**: Replace `/path/to/yourApplication` with the path to the affected application or folder containing multiple blocked files.

** Notes**

- These steps are particularly useful for applications blocked by macOS due to lack of a verified developer signature or for files marked as unsafe because they were downloaded from the internet.
- Always ensure you trust the source of the software you're attempting to run, as bypassing these protections can expose your system to risks.
- This guide is intended to help users quickly resolve issues with running applications that macOS has blocked due to its security settings.


**Linux:**
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
Welcome to GP Analyzer! As you start the application for the first time, here's what you can expect and how to navigate the initial setup process.

**What to Expect:**
- **Console Window**: Upon launching GP Analyzer, a console window will appear. This window is an essential part of the application, providing real-time feedback, status updates, and information about the tasks being performed. It's normal for this console to remain open throughout your use of GP Analyzer, as it will display valuable information during the application's run.
- **Splash Screen (Windows Only)**: Shortly after the console window opens, you'll be greeted by a splash screen. This splash screen serves as a visual indicator that GP Analyzer is in the process of starting up. It's designed to provide a friendly welcome while the application loads the necessary components in the background.
- **Initial Loading Time**: The first startup of GP Analyzer may take some time, which is completely normal and depends on your system's specifications. This initial loading allows GP Analyzer to properly initialize and prepare for optimal performance. We appreciate your patience during this process.
- **GUI Appearance**: Once initialization is complete, the main graphical user interface (GUI) of GP Analyzer will appear. This is where you will interact with the software to load images, perform analyses, and view results. The GUI is designed to be user-friendly and intuitive, providing easy access to all of GP Analyzer's powerful features.
- **Console Window During Use**: As mentioned, the console window will remain open while you use GP Analyzer. It will continue to provide important messages and updates. Keeping an eye on the console can offer insights into the application's processes and alert you to any actions required on your part.

**Getting Started**: With the GUI open, you are now ready to begin exploring GP Analyzer. Whether you're analyzing your first image or configuring settings for your analysis, GP Analyzer is equipped to support your work.

**A Note on Performance**: The performance and responsiveness of GP Analyzer after the initial launch will vary based on the complexity of the tasks you're performing and your computer's hardware. For demanding tasks or large datasets, enhanced system specifications can contribute to smoother operation.

## Navigating the Interface

Welcome to GP Analyzer! This section will help you become familiar with the main window's interface, ensuring you can navigate the software efficiently and make the most out of its powerful features.
![image](https://github.com/biosciflo/VISON/assets/106735259/6072d1b8-ca1c-4484-9741-74ebf34fb299)

### Main Window (1) Overview
The main window of GP Analyzer is designed with intuitiveness and efficiency in mind, structured to facilitate easy access to all necessary tools and functionalities for comprehensive image analysis. Here's what you'll find:

- **Settings Panel (2)**: Positioned to maximize ease of access, the Settings Panel is where you'll begin your journey with GP Analyzer. From top to bottom, it comprises:
  - **Load and Table Interaction Section**: At the very top, this area allows you to load images into GP Analyzer. Following image loading, the section provides functionalities for interacting with the list (table) of loaded images, making it easier to manage and select specific datasets for analysis.
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

### Membrane Settings – P Value and Analysis

- **Channel Settings**: Upon loading image files, fields A, B, C, & D automatically populate with existing channel information, such as '488' or numbers '1-9', derived directly from the original file's metadata. When loading spectral LSM or CZI files, the results in the comboboxes will include all available channel wavelengths.
- **Membrane Profiler**: Enables/disables Membrane Profiler. 
- **Colocalization**: Enables/disables an additional, independent colocalization channel. The population of the combobox below follows the same procedure as described in Channel Settings above.
- **Equation**: The "Equation" text field leverages the channel settings A, B, C, and D to calculate the P-Value, for example, the GP-Value using the formula “(A-B)/(A+B)”. Please note, only the variables A, B, C, and D are permitted in this field.

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
- **Membrane Profiling – P-Value Threshold Auto Cut off** 

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
3. **(Membrane Settings)** (Optional) Enter Equation for P-Value calculation.
4. **(Membrane Settings)** Select Channels for each used variable in Equation.
5. **(Membrane Settings)** (Optional) Enable and Choose Specific Thresholding Channel.
6. **Test Mask** (if Mask is not optimal follow with Steps a-c, otherwise go to 7)
   a. Move displayed Raw Image (Right Panel of Mask Results) to the channel of Choose Specific Thresholding Channel or used Channel of Equation with the lowest intensity. Click on “Probe Raw Image” and select a background area.
   b. Activate Background Compensation.
   c. Test Mask (if Mask is not optimal follow with Steps d-, otherwise go to 7)
   d. Enable options such as the Gauss Filter, Dilation, Compression, and Fill Holes, then fine-tune their respective parameters until the mask is satisfactory. Proceed to Step 7 upon completion.
7. **Run Analysis – (Full Image)**
   a. Check Full Image Results.
8. **Activate Object Detection**
9. **Run Analysis – (Full Image & Object Detection)**
   a. If an error appears in the mini console, try to adapt the Masking options; it could be that the subroutines can't detect single objects.
   b. Check Full Image Results and Object-Related Results.
   
**Note**: Once you have run the image, all Results are automatically Saved.

# Advanced Features

- **Custom Analyses**: Equations???? Different Equations?
- **Patch Processing**: If multiple images are in the Image – List, either:
  - Select Multiple Images and press Run – Selected Images will be Processed.
  Or…
  - Press “Clear Selection” and Press Run - All Images in list will be Processed.

# Troubleshooting and Support

- **Common Issues and Solutions**: As of now, no common issues have been identified. However, we acknowledge that problems we have not yet tested may arise. We appreciate your understanding and patience in these matters. We also encourage you to assist us by reporting any problems you encounter. Your feedback is invaluable in helping us continuously improve the software.
- **Software Updates**: We will release eventually, updates where we cover all the bugs which we and you encounter. New releases you will find here at the GitHub repository.
- **Getting Help**: At the GitHub repository.

# Appendix

- **Glossary**: Definitions of terms and concepts used within the guide and software.
- **FAQs**: Answers to frequently asked questions about the software.

# Index

- **Keyword Index**: An index to help users quickly find information within the guide.


## License

```
MIT License

Copyright (c) 2024 Luca Andronico & Florian Weber

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "VISION"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

