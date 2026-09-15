app.get("/twitter", (req, res) => {
  const usernames = Array.isArray(req.query.username)
    ? req.query.username
    : req.query.username
      ? [req.query.username]
      : [];

  if (usernames.length > 3) {
    return res.status(400).json({
      error: "You can only use up to 3 usernames"
    });
  }

  res.json({
    usernames: usernames,
    count: usernames.length
  });
});
