const postInput = document.querySelector(".postInput");
const postButton = document.querySelector(".submitButton");


postButton.addEventListener("click", () =>{ 
    const text = postInput.value.trim();
    if(!text){ // checks whether there is text or not inside the postInput box
        return;
    }

    // creates the post div
    const newPost = document.createElement("div");
    newPost.classList.add("post");
    
    const reportButton = document.createElement("button");
    reportButton.classList.add("reportButton");
    reportButton.textContent = "Report";

    // adds post content to the post div
    const postContent = document.createElement("p");
    postContent.classList.add("postContent");
    postContent.textContent = text;

    // time the post was made(static, functionality will be added later on)
    const postTime = document.createElement("span");
    postTime.classList.add("postTime")
    postTime.textContent = ("Just now")

    // number of likes(static, functionality will be added later on)
    const likes = document.createElement("span");
    likes.classList.add("likes")
    likes.textContent = "0 likes";

    // like button
    const likeButton = document.createElement("button");
    likeButton.classList.add("likeButton");
    likeButton.textContent = "Like";

    // dislike button
    const dislikeButton = document.createElement("button");
    dislikeButton.classList.add("dislikeButton");
    dislikeButton.textContent = "Dislike";

    // adds text and buttons to the post, but does not add it to the page
    newPost.append(
        reportButton,
        postContent,
        postTime,
        likes,
        likeButton,
        dislikeButton
    );

    // adds the post to the page with every item inside it
    document.querySelector(".posts").prepend(newPost);
});