/********************** Modules **********************/
require("dotenv").config();

const fs = require("fs");
const cors = require("cors");
const path = require("path");
const multer = require("multer");
const express = require("express");

/********************** Variables **********************/
const app = express();

const PORT = process.env.PORT;
const BASE_URL = process.env.BASE_URL;
const UPLOADS_DIR = path.join(__dirname, process.env.UPLOADS_DIR);
const UPLOADS_DIR_TXT = process.env.UPLOADS_DIR;

/********************** Middleware **********************/
app.use(cors())
app.use(express.json())
app.use("/uploads", express.static(UPLOADS_DIR, { redirect: false }));


/********************** Storage Settings **********************/
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        let folder = req.body.location || "/";
        folder = folder.replace(/^\/+/, "");
        const upload_path = path.join(UPLOADS_DIR, folder);

        fs.mkdirSync(upload_path, { recursive: true });
        cb(null, upload_path);
    },
    filename: (req, file, cb) => {
        const filename = req.body.filename;
        cb(null, filename);
    }
});

const upload = multer({ storage });

/********************** Upload File **********************/
app.post("/upload", upload.single("file"), (req, res) => {
    res.status(200).json({ message: "File uploaded!" })
});

/********************** Serve File **********************/
app.post("/get-file-url", (req, res) => {
    // Variables
    const { location } = req.body;

    // Validations
    if (!location) return res.status(400).json({ message: "location is required" });

    // Check if exist
    const full_path = path.join(UPLOADS_DIR, location);

    if (!fs.existsSync(full_path)) {
        return res.status(404).json({ message: "The file does not exist" });
    }

    // Generate URL
    const url_value = `${BASE_URL}:${PORT}/uploads/${location}`;
    return res.status(200).json({ url: url_value });
});

/********************** Download File **********************/
app.post("/download", (req, res) => {
    // Variables
    const { location } = req.body;

    // Validations
    if (!location) return res.status(400).json({ message: "location is required" });

    // Check if exist
    const full_path = path.join(UPLOADS_DIR, location);
    console.log(full_path)

    if (!fs.existsSync(full_path)) return res.status(400).json({ message: "The file does not exist" });

    // Download file
    res.download(full_path, path.basename(full_path), (err) => {
        if (err) {
            console.log("[-] Something went wrong");
            console.log(err);
            if (!res.headersSent) return res.status(400).json({ message: "Error trying to download file" });
        } else {
            console.log("[+] File downloaded");
        }
    })
});

/********************** Delete File **********************/
app.post("/delete", (req, res) => {
    // Variables
    const { location } = req.body;

    // Validations
    if (!location) return res.status(400).json({ message: "location is required" });

    // Check if exist
    const full_path = path.join(UPLOADS_DIR, location);

    if (!fs.existsSync(full_path)) {
        return res.status(404).json({message: "The file does not exist"});
    }

    // Delete file
    try {
        fs.unlinkSync(full_path);
        console.log("[+] File deleted");
        return res.status(200).json({ message: "File deleted successfully" });
    } catch (err) {
        console.log("[-] Error trying to delete the file");
        return res.status(400).json({ message: "Error trying to delete the file" });
    }
});

/********************** Static Files **********************/
// app.use(express.static(path.join(__dirname, 'uploads')));

/********************** Init Server **********************/
app.listen(PORT, () => {
    console.log(`Server running in: ${BASE_URL}:${PORT}`);
});