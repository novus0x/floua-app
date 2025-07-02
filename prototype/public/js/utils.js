/********************** Variables **********************/
const cookie_name = "floua-session";

/********************** DOM Elements **********************/
const video_carousel_template = `
<div class="video-carousel-item">
    <div class="video-carousel-item-thumbail">
        <a href="video_player.html?id={{video_ID}}"><!-- <img src="#" alt="Video preview thumbail"> --></a>
    </div>
    <div class="video-carousel-item-info">
        <a href="#{{video_userID}}" class="video-carousel-item-channel-profile"><!-- <img src="#" alt="Profile"> --></a>
        <div class="video-carousel-item-info-cont">
            <a href="video_player.html?id={{video_ID}}" class="video-carousel-item-title" title="{{video_title}}">{{video_title}}</a>
            <div class="video-carousel-item-channel-info">
                <a href="#$#{{video_userID}}" class="video-carousel-item-channel-name">Channel name</a>
                <span class="video-carousel-item-channel-views">{{video_ID}}</span>
            </div>
        </div>
    </div>
</div>
`;

const video_section_template = `
<div class="content-section-video">
    <div class="content-section-video-thumbail">
        <a href="video_player.html?id={{video_ID}}"><!-- <img src="#" alt="Video preview thumbail"> --></a>
    </div>
    <div class="content-section-video-info">
        <a href="#{{video_userID}}" class="content-section-video-channel-profile"><!-- <img src="#" alt="Profile"> --></a>
        <div class="content-section-video-info-cont">
            <a href="video_player.html?id={{video_ID}}" class="content-section-video-title" title="{{video_title}}">{{video_title}}</a>
            <div class="content-section-video-channel-info">
              <a href="#$#{{video_userID}}" class="content-section-video-channel-name">Channel name</a>
              <span class="content-section-video-channel-views">{{video_ID}}</span>
            </div>
        </div>
    </div>
</div>
`;

const video_search_template = `
<div class="content-search-video">
    <div class="content-search-video-thumbail">
        <a href="video_player.html?id={{video_ID}}"><!-- <img src="#" alt="Video preview thumbail"> --></a>
    </div>
    <div class="content-search-video-info">
        <div class="content-search-video-info-extra">
            <div class="content-search-channel-profile">
                <a href="#{{video_userID}}" class="content-search-video-channel-profile">
                    <!-- <img src="#" alt="Profile"> -->
                </a>
                <a href="#{{video_userID}}" class="content-search-video-channel-name">Channel name</a>
            </div>
            <span class="content-search-video-time">{{time_since}}</span>
        </div>
        <div class="content-search-video-info-detail">
            <a href="video_player.html?id={{video_ID}}" class="content-search-video-title" title="{{video_title}}">{{video_title}}</a>
            <p class="content-search-video-description">{{video_description}}</p>
            <!--<span class="content-search-video-views">{{video_ID}}</span>-->
        </div>
    </div>
</div>
`;

/********************** Utilities **********************/
export function get_cookie(name) {
    const val = `; ${document.cookie}`;
    const parts = val.split(`; ${name}=`);

    if (parts == 2) return parts.pop().split(";").shift();
    return false;
}

export function active_session() {
    const cookie = get_cookie(cookie_name);
    if (cookie) return cookie;
    return false;
}

export function build_query_params(params) {
    const query = new URLSearchParams(params);
    return query.toString() ? `?${query.toString()}` : "";
}

export function get_query_params(url = window.location.href) {
    const query_string = url.includes("?") ? url.split("?")[1].split("#")[0] : "";
    return Object.fromEntries(new URLSearchParams(query_string));
}

export function shorten_text(text, max) {
    const words = text.trim().split(/\s+/);
    if (words.length > max) return words.slice(0, max).join(" ") + "...";
    return text
}

export function format_time(seconds) {
    const h = Math.floor(seconds / 3600);
    seconds -= 3600 * h;
    const m = Math.floor((seconds % 3600) / 60);
    seconds -= 60 * m;
    const s = Math.floor(seconds % 3600);

    if (h > 0) return `${h.toString().padStart(2, "0")}:${m.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}`;
    return `${m.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}`;
}

/********************** DOM **********************/
export function insert_video_carousel(videos, container) {
    videos.forEach((video) => {
        const video_element = video_carousel_template
            .replaceAll("{{video_ID}}", video.id)
            .replaceAll("{{video_userID}}", video.userId)
            .replaceAll("{{video_title}}", video.title);
        container.insertAdjacentHTML('beforeend', video_element);
    });
}

export function insert_video_section(videos, container) {
    videos.forEach((video) => {
        const video_element = video_section_template
            .replaceAll("{{video_ID}}", video.id)
            .replaceAll("{{video_userID}}", video.userId)
            .replaceAll("{{video_title}}", video.title);
        container.insertAdjacentHTML('beforeend', video_element);
    });
}

export function insert_video_search(videos, container) {
    videos.forEach((video) => {
        const video_element = video_search_template
            .replaceAll("{{video_ID}}", video.id)
            .replaceAll("{{video_userID}}", video.userId)
            .replaceAll("{{video_title}}", video.title)
            .replaceAll("{{video_description}}", video.body)
            .replaceAll("{{time_since}}", video.id);
        container.insertAdjacentHTML('beforeend', video_element);
    });
}