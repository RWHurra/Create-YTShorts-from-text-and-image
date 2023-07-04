# Create Youtube Shorts from text and image

## 📖Description

This project is a video generation tool that creates short videos with dad jokes using a combination of images and text. It takes a directory containing a two-part dad joke, an image for the background, and generates a video with the setup and punchline displayed sequentially.

## 💪Motivation

The motivation behind this project is to provide an entertaining and engaging way to share dad jokes on social media platforms like YouTube and TikTok. Dad jokes are popular and often shared in text format, but creating video content adds an extra element of humor and engagement.

## 🚫Problem Solved

This project solves the problem of creating visually appealing videos for dad jokes without the need for advanced video editing skills. By automating the video generation process, users can easily create and share dad joke videos without investing significant time and effort in video editing software.

## 🗝️Key Features

- Automatically creates directories based on a CSV file containing dad jokes.
- Sets up the background image and resizes it according to specified parameters.
- Generates text clips for the joke setup and punchline, including formatting options.
- Adds a black bar as a text background for better visibility.
- Combines all the elements into a final video clip.
- Provides a user-friendly GUI for directory creation. (Work in progress)

## 💻Usage

1. Ensure you have the necessary dependencies installed.
2. Prepare a CSV file with two columns: "Setup" and "Punchline," containing the respective parts of the dad jokes.
3. Place the background image in the same directory as the CSV file.
4. Run the program and select the CSV file to create directories for each joke.
5. Ensure that each joke directory contains a text file with the setup and punchline.
6. Run the program again to generate videos for the jokes that meet the necessary requirements.
7. The output videos will be saved in the respective joke directories.

## 🧑‍🎓Lessons Learned

During the development of this project, several valuable lessons were learned, including:

- Working with movie clips and manipulating video elements using the moviepy library.
- Reading data from CSV files and using it to automate directory creation and text generation.
- Applying formatting options to text clips, such as size, font color, and alignment.
- Using the wxPython library to create a simple graphical user interface for enhanced usability.

## 👉Standout Features

- Automated directory creation based on CSV file input, reducing manual effort and ensuring consistency.
- Text clip setup with customization options for size, color, and alignment.
- Black bar background for improved text visibility.
- User-friendly GUI for easy execution and interaction with the program. (Work in progress)

## Conclusion

This project provides a convenient and efficient way to generate videos for dad jokes, adding an extra layer of entertainment to the popular humor genre. By automating the video generation process and providing customization options, this tool simplifies the creation of engaging dad joke videos.
