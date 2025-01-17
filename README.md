# PhD录取信息爬虫

## 项目概述

该项目是一个自动化的爬虫脚本，用于从GradCafe网站爬取有关PhD项目的录取信息。爬取的数据包括项目的基本信息，如院校名称、学位类型、专业、录取决定、GRE分数等。本脚本通过requests和BeautifulSoup获取网页内容，并解析详细页面上的信息。脚本支持按院校、学位类型、专业、日期等条件进行筛选，输出最终的结果为CSV格式。

## 功能特点

- 搜索并筛选 PhD 项目：根据院校名称、学位类型、专业名称以及起止日期等条件筛选项目。
- 爬取项目详情：获取每个项目的详细信息，包括院校、学位类型、专业、录取决定、GRE成绩、通知日期和方式等。
- 数据存储与更新：爬取的数据会以CSV格式存储，并在每次执行时更新已有数据，避免重复爬取。

## 安装

确保已安装Python 3.x。安装所需包：

```bash
pip install requests beautifulsoup4 pandas selenium
```

此外，下载与Chrome浏览器版本匹配的ChromeDriver，并将其添加到系统路径中。

## 使用方法

### 输入文件格式

在运行爬虫脚本前，首先需要准备一个包含院校名称的Excel或CSV文件。文件的第一行应包含列名"Institution"，并填入需要爬取的院校名称。例如：

| Institution   |
|---------------|
| University A  |
| University B  |
| University C  |

### 配置与运行

确保您已经准备好包含院校信息的文件。运行脚本，在命令行中输入以下命令启动程序：

```bash
python phd_offer_scraper.py
```

根据提示输入：

- 输入文件路径：指定包含院校名称的文件路径（可以是CSV或Excel）。
- 输出文件夹路径：指定爬取结果保存的文件夹。
- 学位类型（PhD/Masters）：如果不限制，直接按回车键跳过。
- 专业名称：如果不限制，直接按回车键跳过。
- 起始日期（YYYY-MM-DD）：如果不限制，直接按回车键跳过。
- 结束日期（YYYY-MM-DD）：如果不限制，直接按回车键跳过。
- 最大爬取页数：如果不限制，直接按回车键跳过。

爬虫会开始爬取GradCafe网站，获取相关PhD项目的录取信息。爬取的数据将会存储在指定的输出文件夹内。

## 输出格式

爬取的结果会保存在CSV文件中，字段包括：

| Institution   | Program   | Degree Type | Country   | Decision   | Notification Date | Notification Method | Undergrad GPA | GRE General | GRE Verbal | Analytical Writing | Notes   | Details URL                        |
|---------------|-----------|-------------|-----------|------------|-------------------|---------------------|---------------|-------------|-------------|-------------------|---------|-----------------------------------|
| University A  | CS        | PhD         | USA       | Admitted   | 2023-08-15        | Email               | 3.8           | 320         | 165         | 4.5               |         | https://gradcafe.com/result/xyz   |
| University B  | Bio       | PhD         | UK        | Waitlisted | 2023-08-17        | Website             | 3.7           | 310         | 160         | 4.0               |         | https://gradcafe.com/result/abc   |

## 说明
- 我已经读过该网址的robots.txt文件，并确认此爬虫在合法合规的范围内运行。我已经爬取了一些数据在本项目的csv文件里，其他人可以运行python脚本爬取他们感兴趣的学校的资料。
- 本项目中已上传CSV文件，包含2023-06-01到2025-01-01之间的部分院校项目部分offer情况。
- 在开始运行爬虫代码前，请确保已创建一个Excel或CSV文件，并在文件的第一行填写“Institution”作为列名。

## 注意事项

- 确保爬取过程遵守GradCafe网站的使用条款。
- 根据网站的反爬虫措施，程序可能会被暂时封锁，建议适当控制请求频率。
- 使用时请确保有足够的磁盘空间来存储爬取的结果。
- 本项目的爬虫代码主要用于个人研究和学习，请勿滥用。

## 贡献

欢迎贡献代码或改进功能。如果你遇到问题或者有新的功能建议，请通过提交Issue或者Pull Request的方式与我们交流。

## 许可

本项目采用MIT开源许可，详情请参考LICENSE文件。

感谢使用本项目！

# PhD Offer Scraper

## Project Overview

This project is an automated web scraper script designed to crawl PhD project admission information from the GradCafe website. The script collects detailed data such as institution name, degree type, major, admission decision, GRE scores, and more. It uses `requests` and `BeautifulSoup` to fetch and parse webpage content, and supports filtering by institution, degree type, major, and date range. The output is stored in a CSV file.

## Features

- **Search and Filter PhD Projects**: Filter projects based on institution, degree type, major, and date range.
- **Scrape Project Details**: Collect detailed information including institution, degree type, major, admission decision, GRE scores, notification date, and method.
- **Data Storage and Update**: Stores crawled data in a CSV file and updates existing data to avoid duplication.

## Installation

Ensure you have Python 3.x installed. Install the required packages using:

```bash
pip install requests beautifulsoup4 pandas selenium
```

Download the appropriate version of ChromeDriver and add it to your system path.

## Usage

### Input File Format

Prepare an Excel or CSV file containing the institutions to be crawled. The file should have a column named "Institution" with the names of the institutions. Example:

| Institution   |
|---------------|
| University A  |
| University B  |
| University C  |

### Running the Script

Execute the script:

```bash
python phd_offer_scraper.py
```

Follow the prompts to input:

- Path to the input file (CSV or Excel).
- Output folder path for results.
- Optional filters: degree type, major, date range, and maximum pages to crawl.

## Output Format

The output CSV file will include the following fields:

| Institution   | Program   | Degree Type | Country   | Decision   | Notification Date | Notification Method | Undergrad GPA | GRE General | GRE Verbal | Analytical Writing | Notes   | Details URL                        |
|---------------|-----------|-------------|-----------|------------|-------------------|---------------------|---------------|-------------|-------------|-------------------|---------|-----------------------------------|
| University A  | CS        | PhD         | USA       | Admitted   | 2023-08-15        | Email               | 3.8           | 320         | 165         | 4.5               |         | https://gradcafe.com/result/xyz   |
| University B  | Bio       | PhD         | UK        | Waitlisted | 2023-08-17        | Website             | 3.7           | 310         | 160         | 4.0               |         | https://gradcafe.com/result/abc   |

## Notes
- I have reviewed the robots.txt file and confirm that this crawler operates within legal and compliant boundaries. I have already crawled some data, and others can run the python script to crawl data for schools they are interested in.
- This project includes a CSV file with data from 2023-06-01 to 2025-01-01.
- Prepare the input file with the "Institution" column before running the script.
- Ensure compliance with GradCafe's terms of use.
- Be mindful of potential IP blocking; control request frequency.
- Ensure sufficient disk space for storing results.
- Intended for personal research and learning purposes.

## Contributions

Contributions are welcome. Report issues or suggest new features via pull requests or issues.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

Thank you for using this project!
