# AoE2 Taunt Soundboard

Static Age of Empires II taunt soundboard. Open `index.html`, or serve this folder with any static file server. Taunt audio lives in `taunts/`.

## Privacy

The page loads the Cinzel and Merriweather fonts from Google Fonts (`fonts.googleapis.com` and `fonts.gstatic.com`). Opening the site sends that font request straight to Google, including the visitor's IP address and usual browser information such as the User-Agent. Google describes how it handles that data in its [privacy policy](https://policies.google.com/privacy) and the [Google Fonts FAQ](https://developers.google.com/fonts/faq).

This note lives in the repository only. The site itself does not show a privacy banner.

### Self-hosting the fonts

A fork that should not contact Google can serve the same faces locally:

1. Download Cinzel (weights 600 and 700) and Merriweather (weights 400 and 700) from [Google Fonts](https://fonts.google.com/) or the [google/fonts](https://github.com/google/fonts) repository, and commit the files (for example under `fonts/`).
2. Add a stylesheet that points at those files with `@font-face`.
3. In `index.html`, remove the preconnect and stylesheet links for `fonts.googleapis.com` and `fonts.gstatic.com`, and link the local stylesheet instead.

The soundboard does not need any other third-party request.
