const express = require("express");

const app = express();
const PORT = process.env.PORT || 3000;

app.get("/", (req, res) => {
  res.json({
    status: "online",
    message: "Twitter API is running"
  });
});

app.get("/tweet", async (req, res) => {
  try {
    const tweetUrl = req.query.url;

    if (!tweetUrl) {
      return res.status(400).json({
        error: "Missing tweet URL"
      });
    }

    const match = tweetUrl.match(/status\/(\d+)/);

    if (!match) {
      return res.status(400).json({
        error: "Invalid X/Twitter URL"
      });
    }

    const tweetId = match[1];

    const response = await fetch(
      `https://api.fxtwitter.com/status/${tweetId}`
    );

    const data = await response.json();

    if (!data.response || !data.response.tweet) {
      return res.status(404).json({
        error: "Tweet not found"
      });
    }

    const tweet = data.response.tweet;

    res.json({
      text: tweet.text,
      url: tweet.url,
      image: tweet.media?.photos?.[0]?.url || "",
      username: tweet.author?.screen_name || ""
    });

  } catch (error) {
    res.status(500).json({
      error: "Failed to fetch tweet"
    });
  }
});

app.listen(PORT, () => {
  console.log(`Twitter API running on port ${PORT}`);
});
