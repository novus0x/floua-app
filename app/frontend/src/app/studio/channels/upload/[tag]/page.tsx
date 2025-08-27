'use client';

/********************** Modules **********************/
import React, { useRef } from "react";
import { useRouter } from "next/navigation";
import { use, useState, useEffect } from "react";

// DOM
import Link from "next/link";
import Player from "@/components/Player";

// Icons
import { RiUploadCloud2Line, RiVideoLine } from "react-icons/ri";

// Routes
import { routes } from "@/helpers/routes";

// Auth
import { useAuth } from "@/context/auth";

// Settings
import { settings } from "@/helpers/settings";

// Notifications
import { useNotification } from "@/context/notifications";

// API
import { get_data, send_data, send_files } from "@/helpers/api";

// Utils
import { creators_only } from "@/helpers/utils";

/********************** Upload **********************/
const Upload = ({ params }: { params: Promise<{ tag: string }> }) => {
    // Notifications
    const { notify } = useNotification();

    // Auth
    const { user } = useAuth();

    // Router
    const router = useRouter();

    // Query
    let { tag } = use(params);
    tag = decodeURIComponent(tag);

    // Structure

    // States
    const [dragActive, setDragActive] = useState(false);
    const [videoFile, setVideoFile] = useState<File | null>(null);
    const [videoSrc, setVideoSrc] = useState<string | null>(null);
    const [readyToUpload, setReadyToUpload] = useState(false);
    const [loading, setLoading] = useState(false);

    const [source, setSource] = useState("cdn");

    // Reference
    const input_file_ref = useRef<HTMLInputElement>(null);
    const container_ref = useRef<HTMLDivElement>(null);

    // Variables
    let check_role = false;

    // Role
    useEffect(() => {
        // 
        if (!check_role) {
            creators_only(user, notify, "Create your channel to start using Floua Studio");
            check_role = true;
        }
    }, [creators_only]);

    // Functions
    const handle_drag = (e: React.DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        e.stopPropagation();

        if (e.type === "dragenter" || e.type === "dragover") setDragActive(true);
        else if (e.type === "dragleave") setDragActive(false);
    };

    const handle_drop = (e: React.DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);

        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('video/')) {
            setReadyToUpload(true);
            setVideoFile(file);
        } else {
            notify("Only video files are allowed", "alert");
        }
    };

    const handle_file_change = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];

        if (file && file.type.startsWith("video/")) {
            setReadyToUpload(true);
            setVideoFile(file);
        } else {
            notify("Only video files are allowed", "alert");
        }
    };

    const handle_click = () => {
        input_file_ref.current?.click();
    };

    const handle_source = (e: React.ChangeEvent<HTMLSelectElement>) => {
        setSource(e.target.value);
    };

    // Change video
    useEffect(() => {
        if (!videoFile) {
            setVideoSrc(null);
            return;
        }

        const url = URL.createObjectURL(videoFile);
        setVideoSrc(url);

        return () => {
            URL.revokeObjectURL(url);
        }
    }, [videoFile]);

    // Upload Video
    const handle_upload = async () => {
        if (!videoFile) {
            notify("Please select your video!", "alert");
            setReadyToUpload(false);
            return;
        }
        if (!container_ref.current || loading) return;
        setLoading(true);
        const elements = container_ref.current.querySelectorAll('input, select, textarea');
        const values: Record<string, string> = {};

        // Variables
        let ready = true;

        elements.forEach((e) => {
            const field = e as HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement;
            if (field.name && field.type !== "file") {
                values[field.name] = field.value;
                if (field.type == "text" || field.type == "select-one") {
                    if (!field.value) {
                        notify(`${field.name.charAt(0).toUpperCase() + field.name.slice(1)} is required`, "alert");
                        ready = false;
                    }
                } else if (field.type == "textarea") {
                    if (field.value == "") values[field.name] = "No description.";
                }
            }
        })

        if (!ready) {
            setLoading(false);
            return;
        };

        const data = await send_data(`/api/studio/channel/${tag}/upload`, {}, values, notify, true);

        if (!data) {
            setLoading(false);
            return;
        };

        const formData = new FormData();
        formData.append("file", videoFile);
        formData.append("upload_token", data.upload_token);

        const submit_video = await send_files(data.destination, {}, formData);
        console.log(submit_video);
        if (!submit_video?.status) {
            notify("Something went wrong, try again later!");
            return window.location.href = routes.studio.channels.manage_tag(tag);
        } else if (submit_video.status == "Uploaded") {
            notify("Video uploaded!", "success");
            return window.location.href = routes.studio.channels.check_upload_tag(tag, data.short_id)
        }
    }

    // DOM
    return (
        <div className="studio-content" ref={container_ref}>
            <div className="studio-content-breadcrumps-extra-container">
                <div className="studio-content-breadcrumps">
                    <Link href={routes.studio.home}>Home</Link> / <Link href={routes.studio.channels.manage}>Channel</Link> / <Link href={routes.studio.channels.manage_tag(tag)}>{tag}</Link> / <span className="studio-content-breadcrumps-active">Upload</span>
                </div>
                <div>

                </div>
            </div>

            <div className="studio-content-upload">
                <div className="studio-content-upload-left">
                    <div className="studio-content-upload-input-container">
                        <span>Title</span>
                        <input type="text" name="title" placeholder="Title" className="studio-content-upload-input" />
                    </div>
                    <div className="studio-content-upload-input-container">
                        <span>Description</span>
                        <textarea name="description" placeholder="Description (Optional)" className="studio-content-upload-input"></textarea>
                    </div>
                    <div className="studio-content-upload-input-container">
                        <span>Visibility</span>
                        <select name="visibility" className="studio-content-upload-input studio-content-upload-select">
                            <option value="public" className="studio-content-upload-input-option" defaultChecked>Public</option>
                            <option value="private" className="studio-content-upload-input-option">Private</option>
                            <option value="unlisted" className="studio-content-upload-input-option">Unlisted</option>
                        </select>
                    </div>
                    <div className="studio-content-upload-input-container">
                        <span>Contracts</span>
                        <select name="contract" className="studio-content-upload-input studio-content-upload-select">
                            <option value="unavailable" className="studio-content-upload-input-option" defaultChecked>No Contracts available</option>
                        </select>
                    </div>
                    <div className="studio-content-upload-input-container">
                        <button disabled={!readyToUpload || loading} className={`studio-content-upload-btn ${readyToUpload && !loading ? "" : "studio-content-upload-btn-disabled"}`} onClick={handle_upload}>{loading ? "Uploading Video..." : "Upload Video"}</button>
                    </div>
                </div>

                <div className="studio-content-upload-right">
                    <div className="studio-content-upload-input-container">
                        <span>Source</span>
                        <select name="source" className="studio-content-upload-input studio-content-upload-select" onChange={handle_source}>
                            <option value="cdn" className="studio-content-upload-input-option" defaultChecked>Floua</option>
                            <option value="youtube" className="studio-content-upload-input-option">Youtube</option>
                            <option value="external" className="studio-content-upload-input-option">External</option>
                        </select>
                    </div>
                    {source == "cdn" && (
                        <div className={`studio-content-upload-video-container ${videoFile ? "studio-content-upload-video-container-change" : ""}`} onClick={handle_click} onDragEnter={handle_drag} onDragOver={handle_drag} onDragLeave={handle_drag} onDrop={handle_drop}>
                            <input type="file" onChange={handle_file_change} ref={input_file_ref} className="hidden" accept="video/*" />
                            <div className="studio-content-upload-video-info">

                                {videoFile ? (
                                    <>
                                        <RiVideoLine size={32} />
                                        <span className="studio-content-upload-video-info-text">Video ready!</span>
                                        <span>Drop your video here or click to change it!</span>
                                    </>
                                ) : (
                                    <>
                                        <RiUploadCloud2Line size={32} />
                                        <span className="studio-content-upload-video-info-text">Drop your video here or click to upload!</span>
                                    </>
                                )}
                            </div>
                        </div>
                    )}

                    {source == "youtube" && (
                        <h3>Youtube</h3>
                    )}

                    {source == "external" && (
                        <h3>External</h3>
                    )}
                </div>
            </div>

            {videoFile && source == "cdn" && (
                <div>
                    {videoSrc && (
                        <Player key={videoSrc} videoSrc={videoSrc} preview />
                    )}
                </div>
            )}

        </div>
    );
};

export default Upload;