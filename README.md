scratch_batch_import

通过 Python 一键为 Scratch 项目批量导入角色造型，适合需要一次性导入大量图片的用户。
 
📁 主要项目结构

scratch_batch_import/
├── images/                                   # 图片存放文件夹
│   └── （在这里放图片）        # （文字提示）
├── （在这里放作品文件）
├── import_costumes.py                        # 核心运行脚本
├── main.bat                                  # Windows 一键运行程序

📌 使用教程
 
1. 安装依赖
 
使用前需要先安装图片处理库，打开命令提示符（CMD）执行命令：
 
bash
  
pip install pillow
 
 
也可以直接查看项目内的  please "pip install pillow" first.txt  文件。
 
2. 准备文件
 
1. 将你的 .sb3 格式 Scratch 项目文件 直接放在项目根目录（提示文字仅作说明，不用新建文件夹）。
2. 将需要导入的图片放入  images  文件夹，支持格式： .png 、 .jpg 、 .jpeg 、 .svg 。
 
3. 运行程序
 
- Windows 系统：直接双击  main.bat  运行
- 其他系统：在终端中执行以下命令
  
python import_costumes.py
 
4. 按照提示操作
 
1. 启动后选择语言： zh （中文）或  en （英文）
2. 输入你的 sb3 项目文件名
3. 输入需要添加造型的目标角色名称
4. 程序运行完毕后，会在根目录生成新项目文件，命名格式为  原文件名_批量导入.sb3 
 
 
 
📄 开源说明
 
本项目遵循 Apache License 2.0 开源规则，相关完整内容请查看仓库内的  LICENSE  文件。

scratch_batch_import
 
One-click bulk import of costumes for Scratch projects via Python. Perfect for users who need to import a large number of images at once.
 
📁 Main Project Structure
 
plaintext
  
scratch_batch_import/
├── images/                                   # Folder for storing images
│   └── (Put images here)                     # Text reminder only
├── (Put project files here)                  # Text reminder only
├── import_costumes.py                        # Main script
├── main.bat                                  # One-click launcher for Windows 
 
📌 Usage Guide
 
1. Install Dependencies
 
Install the image processing library before use. Run the command in Command Prompt (CMD):
 
bash
  
pip install pillow
 
 
You can also refer to the file named  please "pip install pillow" first.txt  in the project.
 
2. Prepare Files
 
1. Place your Scratch project file in  .sb3  format directly in the project root directory. The text above is just a reminder, no extra folder is required.
2. Put your images into the  images  folder. Supported formats:  .png ,  .jpg ,  .jpeg ,  .svg .
 
3. Run the Program
 
- Windows: Double-click  main.bat  to launch
- Other systems: Run the command below in terminal
 
bash
  
python import_costumes.py
 
 
4. Follow On-screen Instructions
 
1. Select language after launch:  zh  (Chinese) or  en  (English)
2. Enter the name of your sb3 project file
3. Enter the name of the target sprite to add costumes to
4. A new project file will be generated in the root directory when completed, named as  OriginalFileName_batch_import.sb3 
 
📄 Open Source Notice
 
This project follows the Apache License 2.0. For full terms, please check the  LICENSE  file in the repository.
