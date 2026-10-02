const postInput = document.querySelector(".postInput");
const postButton = document.querySelector(".submitButton");

function createPostElement(post){
    
    // creates the post div
    const newPost = document.createElement("div");
    newPost.classList.add("post");
    
    const reportButton = document.createElement("button");
    reportButton.classList.add("reportButton");
    reportButton.textContent = "Report";

    // adds post content to the post div
    const postContent = document.createElement("p");
    postContent.classList.add("postContent");
    postContent.textContent = post.content;

    // time the post was made(static, functionality will be added later on)
    const postTime = document.createElement("span");
    postTime.classList.add("postTime");
    postTime.textContent = post.createdAt;

    // like button
    const likeButton = document.createElement("button");
    likeButton.classList.add("likeButton");
    likeButton.textContent = "Like";

    // number of likes(static, functionality will be added later on)
    let numberofLikes = post.likes;
    const likes = document.createElement("span");
    likes.classList.add("likes")
    likes.textContent =  numberofLikes + " likes";
    likeButton.addEventListener("click", () => {
        numberofLikes += 1;
        likes.textContent =  numberofLikes + " likes";
    });
    
    // dislike button
    const dislikeButton = document.createElement("button");
    dislikeButton.classList.add("dislikeButton");
    dislikeButton.textContent = "Dislike";
    dislikeButton.addEventListener("click", () =>{
        numberofLikes -= 1;
        likes.textContent = numberofLikes + " likes";
    });

    // adds text and buttons to the post, but does not add it to the page
    newPost.append(
        reportButton,
        postContent,
        postTime,
        likes,
        likeButton,
        dislikeButton
    );

    return newPost;
}

async function fetchPosts(){ // fetches posts from the API
    try{
        const response = await fetch("/api/posts");
        if(!response.ok){
            throw new Error(`Could not load posts: ${response.status}`);
        }

        const posts = await response.json();
        const postContainer = document.querySelector(".posts");

        for(const post of posts){
            postContainer.append(createPostElement(post));
        }
    }
    catch(error){
        console.error("Failed to posts: ", error);
    }
} fetchPosts();

postButton.addEventListener("click", () =>{ 
    const text = postInput.value.trim();
    if(!text){ // checks whether there is text or not inside the postInput box
        return;
    }
    
    const newPost = createPostElement({
        content: text,
        createdAt: "Just now",
        likes: 0
    });

    // adds the post to the page with every item inside it
    document.querySelector(".posts").prepend(newPost);
});