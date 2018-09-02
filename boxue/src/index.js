const fs = require('fs');
const axios = require('axios');
const puppeteer = require('puppeteer');
const youtubedl = require('youtube-dl');
const log4js = require('log4js');
log4js.configure({
    appenders: {
        'file': { type: 'file', filename: 'log/boxue.log' },
        'console': { type: 'console' }
    },
    categories: {
        default: { appenders: ['file', 'console'], level: 'debug' },
        'monkeyCC': { appenders: ['file', 'console'], level: 'debug' }
    }
});

var { timeout } = require('../tools/tools.js');
var videos = [];
const username = "----";
const password = "----";
const logger = log4js.getLogger('monkeyCC');
const saveDir = "/Users/yaoning/Documents/boxue/"

/**
 *  获取所有视频元数据
 */
async function loadAllVideoMetadata() {
    try {
        videos = await readJson(saveDir + "/allVedio.json");
        logger.info("缓存 获取视频元数据成功 总计" + videos.length + "个视频");
        return
    } catch (error) {
        logger.info("缓存获取失败 " + error)
    }
    let pageCount = 28;
    logger.info("获取视频元数据 总计" + pageCount + "页");
    for (var i = 1; i <= pageCount; i++) {
        logger.info("获取第" + i + "页");
        if (i == 24) {
            continue;
        }
        const page = await axios("https://boxueio.com/recent-update/" + i + "/15");
        if (page.status == 200) {
            let array = page.data["episodes"];
            videos = videos.concat(array);
        }
        await timeout(1000);
    }
    await writeJson(videos, saveDir + "/allVedio.json");
    logger.info("获取视频元数据成功 总计" + videos.length + "个视频");
}

/**
 *  浏览视频详情页
 *
 */
async function visitVedioDetail() {
    const browser = await puppeteer.launch({
        executablePath: '/Applications/Chromium.app/Contents/MacOS/Chromium',
        headless: true
    });
    const page = await browser.newPage();
    const override = Object.assign(page.viewport(), { width: 1366, height: 500 });
    await page.setViewport(override);

    await loginBoxue(page);

    for (var i = 0; i < videos.length; i++) {
        let video = videos[i];
        let href = "https://boxueio.com" + video["episode_url"];
        logger.info("------------------------------------------------------------")
        logger.info(i + " 访问视频详情页 id:" + video["id"] + " 标题:" + video["title"] + " 详情页地址:" + href);
        await page.goto(href);
        let vedioDownloadUrl = await page.evaluate(() => {
            let href = document.querySelector('.u-btn-teal.g-font-weight-600').href
            return href
        });
        let documentDownloadUrl = await page.evaluate(() => {
            let href = document.querySelector('.u-btn-indigo.g-font-weight-600').href
            if (href.startsWith('https://boxueio.com')) {
                return href
            }
            return "https://boxueio.com" + href
        });

        let seriesName = video["series_title"].replace(' ', '_');
        let fileName = video["episode_title"];
        let seriesDir = saveDir + seriesName;
        let vedioSavePath = seriesDir + "/" + fileName + ".mp4";
        let jsonSavePath = seriesDir + "/" + fileName + ".json";
        let pdfSavePath = seriesDir + "/" + fileName + ".pdf";
        await mkdirIfNeed(seriesDir);
        await downloadVedio(vedioDownloadUrl, vedioSavePath);
        await writeJson(video, jsonSavePath);
        await document2Pdf(documentDownloadUrl, pdfSavePath, page);
        await timeout(4000);
    }
    await browser.close();
}

/**
 *  下载视频
 *
 * @param {*} downloadUrl   下载地址
 * @param {*} savePath      本地保存地址
 * @returns
 */
function downloadVedio(downloadUrl, savePath) {
    return new Promise((resolve, reject) => {
        var video = youtubedl(downloadUrl);
        video.on('info', function (info) {
            logger.info("下载视频 源路径:" + downloadUrl + " 目标路径:" + savePath + " 文件大小:" + (info.size / (1024 * 1024)).toFixed(2) + "M");
        });
        video.on('end', function (info) {
            logger.info("下载完毕");
            resolve();
        });
        video.on('error', function (info) {
            logger.error("下载失败 " + downloadUrl);
            reject();
        })
        video.pipe(fs.createWriteStream(savePath));
    })
}

/**
 *  视频文档转PDF
 *
 * @param {*} downloadUrl
 * @param {*} savePath
 * @param {*} page
 */
async function document2Pdf(downloadUrl, savePath, page) {
    logger.info("保存网页到PDF 源路径:" + downloadUrl + " 目标路径:" + savePath);
    await page.goto(downloadUrl);
    await timeout(2000);
    await page.pdf({ path: savePath });
    logger.info("保存网页到PDF 完毕");
}

/**
 *  写JSON
 *
 * @param {*} object
 * @param {*} savePath
 * @returns
 */
function writeJson(object, savePath) {
    return new Promise((reslove, reject) => {
        fs.writeFile(savePath, JSON.stringify(object), function (err) {
            reslove();
        });
    })
}

/**
 *  读JSON
 *
 * @param {*} path
 */
function readJson(path) {
    return new Promise((reslove, reject) => {
        fs.readFile(path, function (err, data) {
            if (err) {
                reject()
            } else {
                reslove(JSON.parse(data))
            }
        })
    })
}

/**
 *  创建文件夹
 *
 * @param {*} filePath
 * @returns
 */
function mkdirIfNeed(filePath) {
    return new Promise((resolve, reject) => {
        fs.mkdir(filePath, function (err) {
            if (err) {
            }
            resolve();
        })
    })
}

/**
 *  登录泊学
 *
 * @param {*} page
 */
async function loginBoxue(page) {
    logger.info("登录泊学");
    await page.goto("https://boxueio.com/");
    await page.click('#navBar > ul > li:nth-child(7) > a');
    await page.type('#ModelLogin > div:nth-child(2) > div > div > form > div:nth-child(1) > input', username, { delay: 20 });
    await page.type('#ModelLogin > div:nth-child(2) > div > div > form > div:nth-child(2) > input', password, { delay: 20 });
    await page.click('#ModelLogin > div:nth-child(2) > div > div > form > button');
    logger.info("登录完毕 歇3s 等待浏览器同步登录信息");
    await timeout(3000);
}

/**
 *  入口
 *  
 */
async function main() {
    await loadAllVideoMetadata();
    await visitVedioDetail();
}

main();