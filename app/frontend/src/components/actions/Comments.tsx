'use client';

/********************** Modules **********************/
import { useRouter } from "next/navigation";
import { useState, useEffect, useRef } from "react";

// DOM
import Link from "next/link";

// Icons
import { MdKeyboardArrowRight, MdKeyboardArrowLeft } from "react-icons/md";

// Auth
import { useAuth } from "@/context/auth";

// Routes
import { routes } from "@/helpers/routes";

// Notifications
import { useNotification } from "@/context/notifications";

// API
import { get_data, send_data } from "@/helpers/api";

// Structure
interface CommentsProps {
    id: string,
}

/********************** Home **********************/
const Comments = ({ id }: CommentsProps) => {
    // Auth
    const { user } = useAuth();

    // Router
    const router = useRouter();

    // Structures
    interface UserComment {
        id: string,
        username: string,
        avatar_url: string,
    }

    interface Comment {
        id: string,
        parent_id: string,
        content: string,
        date: string,

        user: UserComment,
    }

    // States
    const [newCommentInput, setNewCommentInput] = useState(false);
    const [newCommentValue, setNewCommentValue] = useState("");

    const [comments, setComments] = useState<Comment[]>([]);

    // Refs
    const commentRef = useRef<HTMLTextAreaElement>(null);

    // Variables
    let alreadyRequestComments = false;

    // Functions
    const newCommentHandleClick = () => {
        setNewCommentInput(true);
    };

    const newCommentHandleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setNewCommentValue(e.target.value);
    }

    const newCommentCancel = () => {
        setNewCommentInput(false);

        if (commentRef.current) {
            setNewCommentValue("");
            commentRef.current.value = "";
        }
    }

    const newCommentCreate = async () => {
        setNewCommentInput(false);

        if (commentRef.current) {
            await send_data(`/api/videos/comments/${id}`, {}, {
                content: newCommentValue,
                parent_id: "none"
            })

            setNewCommentValue("");
            commentRef.current.value = "";

            await get_comments();
        }
    }

    const get_comments = async () => {
        const data = await get_data(`/api/videos/comments/${id}`, {});
        if (data?.comments) {
            setComments(data.comments);
        }
    }

    // Effects
    useEffect(() => {
        const textarea = commentRef.current;

        if (textarea) {
            textarea.style.height = 'auto';
            textarea.style.height = `${textarea.scrollHeight}px`;
        }
    }, [newCommentValue])

    // API
    useEffect(() => {
        if (!alreadyRequestComments) {
            get_comments();
            alreadyRequestComments = true;
        }
    }, [])

    // DOM
    return (
        <div className="floua-comments-container">
            {user ? (
                <div className="floua-comments-comment">
                    <div className="floua-comments-comment-avatar">
                        <img src={user.avatar_url} alt="User avatar" />
                    </div>
                    <div className="floua-comments-comment-info">
                        <span className="floua-comments-comment-info-username">{user.username}</span>
                        <textarea ref={commentRef} rows={1} placeholder="Add a comment!" className="floua-comments-create-input" onClick={newCommentHandleClick} onChange={newCommentHandleChange} />
                        <div className={`floua-comments-comment-actions-container ${newCommentInput ? "" : "hidden"}`}>
                            <button className="floua-comments-comment-action floua-comments-comment-action-cancel" onClick={newCommentCancel}>Cancel</button>
                            <button className="floua-comments-comment-action floua-comments-comment-action-comment" onClick={newCommentCreate}>Add Comment!</button>
                        </div>
                    </div>
                </div>
            ) : (
                <></>
            )}
            {comments.map(comment => (
                <div className="floua-comments-comment" key={comment.id}>
                    <div className="floua-comments-comment-avatar">
                        <img src={comment.user.avatar_url} alt="User avatar" />
                    </div>
                    <div className="floua-comments-comment-info">
                        <span className="floua-comments-comment-info-username">{comment.user.username}</span>
                        <div className="floua-comments-comment-info-text">{comment.content}</div>
                    </div>
                </div>
            ))}
        </div>
    );
};

export default Comments;
