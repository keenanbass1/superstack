# Accessible Images and Media

Images, videos, and audio content need special consideration to ensure they're accessible to all users, including those with visual or auditory impairments.

## Images

### Alternative Text

All images that convey information must have alternative text:

```html
<!-- Informative image with alt text -->
<img src="chart.png" alt="Bar chart showing sales increasing by 25% in Q4 2024">
```

The alt text should:
- Be concise but descriptive
- Convey the purpose and content of the image
- Not start with "Image of" or "Picture of"
- Include any text that appears in the image

### Decorative Images

Images that are purely decorative should have empty alt text:

```html
<!-- Decorative image with empty alt -->
<img src="decorative-divider.png" alt="">

<!-- Or using CSS instead (preferred for purely decorative images) -->
<div class="decorative-divider" aria-hidden="true"></div>
```

### Complex Images

For complex images like charts, graphs, or diagrams:

```html
<!-- Complex image with brief alt and longer description -->
<figure>
  <img 
    src="complex-chart.png" 
    alt="Q4 2024 sales performance by region" 
    aria-describedby="chart-desc">
  <figcaption id="chart-desc">
    Chart showing quarterly sales performance across regions. North America 
    leads with $1.2M (up 15%), followed by Europe at $800K (up 10%), and 
    Asia at $600K (up 25%). Overall growth is 18% year-over-year.
  </figcaption>
</figure>
```

### Images of Text

Avoid using images of text when possible. If necessary:

```html
<img 
  src="quote.png" 
  alt="The best way to predict the future is to create it. - Abraham Lincoln">
```

### SVG Images

Make SVGs accessible:

```html
<!-- Accessible SVG -->
<svg role="img" aria-labelledby="svg-title svg-desc">
  <title id="svg-title">Company Growth Chart</title>
  <desc id="svg-desc">Line graph showing steady growth from 2020 to 2025</desc>
  <!-- SVG content -->
</svg>
```

### Image Maps

For image maps:

```html
<img 
  src="map.png" 
  alt="Map of our office locations" 
  usemap="#office-map">

<map name="office-map">
  <area 
    shape="rect" 
    coords="12,14,90,82" 
    href="new-york.html" 
    alt="New York Office">
  <area 
    shape="rect" 
    coords="120,14,200,82" 
    href="london.html" 
    alt="London Office">
  <area 
    shape="rect" 
    coords="252,14,320,82" 
    href="tokyo.html" 
    alt="Tokyo Office">
</map>
```

## Video

### Video with Audio

Videos with audio should have:
1. Captions for deaf or hard-of-hearing users
2. Audio descriptions for blind or low-vision users
3. Transcript for deaf-blind users

```html
<figure>
  <video controls>
    <source src="video.mp4" type="video/mp4">
    <track 
      src="captions.vtt" 
      kind="subtitles" 
      srclang="en" 
      label="English" 
      default>
    <track 
      src="descriptions.vtt" 
      kind="descriptions" 
      srclang="en" 
      label="Audio Descriptions">
    Your browser does not support the video tag.
  </video>
  
  <figcaption>
    <details>
      <summary>Transcript</summary>
      <div>
        <p><strong>Narrator:</strong> In this tutorial, we'll explore...</p>
        <p><strong>Speaker 1:</strong> The first step is to...</p>
        <!-- Full transcript -->
      </div>
    </details>
  </figcaption>
</figure>
```

### Captions

Captions should:
- Include all spoken dialogue
- Identify speakers when there are multiple
- Include relevant non-speech sounds (e.g., [laughter], [doorbell rings])
- Be synchronized with the video

WebVTT format example:

```
WEBVTT

00:00:01.000 --> 00:00:04.000
Narrator: Welcome to our product demonstration.

00:00:05.000 --> 00:00:08.000
Today we'll show you how to set up your new device.

00:00:10.000 --> 00:00:12.000
[background music playing]
```

### Audio Descriptions

Audio descriptions narrate the important visual elements that aren't conveyed through dialogue:

```
WEBVTT

00:00:20.000 --> 00:00:22.000
[Woman points to the red button on device]

00:00:35.000 --> 00:00:37.000
[Screen displays error message: "Battery low"]

00:00:50.000 --> 00:00:52.000
[Man smiles and gives thumbs up as device turns on]
```

### Video Player Accessibility

Ensure video players have:
- Keyboard accessible controls
- Visible focus states
- Clear labels for controls
- Volume control
- Playback speed control

```html
<div class="video-player">
  <video id="my-video" tabindex="-1">
    <source src="video.mp4" type="video/mp4">
  </video>
  
  <div class="video-controls">
    <button aria-label="Play video" id="play-button">
      <span class="icon" aria-hidden="true">▶</span>
    </button>
    
    <div class="time-display" aria-live="polite">
      <span id="current-time">0:00</span> / <span id="duration">5:30</span>
    </div>
    
    <div class="progress-bar">
      <label for="progress" class="sr-only">Video progress</label>
      <input 
        type="range" 
        id="progress" 
        min="0" 
        max="100" 
        value="0" 
        aria-valuemin="0" 
        aria-valuemax="100" 
        aria-valuenow="0">
    </div>
    
    <button aria-label="Mute" id="mute-button">
      <span class="icon" aria-hidden="true">🔊</span>
    </button>
    
    <button aria-label="Enable captions" id="caption-button">
      <span class="icon" aria-hidden="true">CC</span>
    </button>
  </div>
</div>
```

### Silent Videos

For videos without audio (like animations):

```html
<figure>
  <video 
    autoplay 
    loop 
    muted 
    aria-describedby="animation-desc">
    <source src="animation.mp4" type="video/mp4">
  </video>
  <figcaption id="animation-desc">
    Animation showing how the app transforms photos into sketches:
    a photo enters on the left, passes through a filter, and emerges
    as a sketch on the right.
  </figcaption>
</figure>
```

## Audio

### Audio Controls

All audio should:
- Have playback controls
- Not play automatically (or stop within 3 seconds)

```html
<figure>
  <audio controls>
    <source src="podcast.mp3" type="audio/mpeg">
    Your browser does not support the audio element.
  </audio>
  
  <figcaption>
    <h3>Interview with Design Director</h3>
    <details>
      <summary>Transcript</summary>
      <div>
        <p><strong>Host:</strong> Welcome to our design podcast...</p>
        <p><strong>Guest:</strong> Thank you for having me...</p>
        <!-- Full transcript -->
      </div>
    </details>
  </figcaption>
</figure>
```

### Alternative for Audio

Always provide a text transcript:

```html
<audio controls>
  <source src="instructions.mp3" type="audio/mpeg">
  Your browser does not support the audio element.
</audio>

<h3>Audio Transcript</h3>
<p>
  Welcome to the installation instructions for your new device.
  First, remove all items from the box. You should find:
  the main unit, power cable, remote control, and quick start guide.
</p>
<p>
  Next, connect the power cable to the back of the unit and plug
  it into a wall outlet. Press the power button on the top right
  corner of the device.
</p>
```

## General Media Accessibility Principles

1. **Always provide alternatives**: Text alternatives for visual content, visual/text alternatives for audio content
2. **Give user control**: Allow pausing, stopping, adjusting volume
3. **Avoid autoplay**: Don't start media automatically, especially with sound
4. **Consider bandwidth**: Provide options for different connection speeds
5. **Test with assistive technology**: Verify accessibility with screen readers and other tools

## Common Media Accessibility Issues

1. **Missing alt text**: Images without alternative text
2. **Uninformative alt text**: Alt text that doesn't adequately describe the image
3. **Missing captions**: Videos without captions for deaf or hard-of-hearing users
4. **Missing audio descriptions**: Videos that don't describe visual content for blind users
5. **Autoplay media**: Media that starts automatically with sound
6. **Inaccessible controls**: Media players that can't be operated by keyboard
7. **Flash content**: Content that flashes more than 3 times per second (seizure risk)

## Testing Media Accessibility

1. **Screen reader test**: Use a screen reader to verify all media has proper alternatives
2. **Keyboard test**: Ensure all player controls are keyboard accessible
3. **Caption quality**: Review captions for accuracy and synchronization
4. **Play with sound off**: Verify understanding of video with sound off and captions on
5. **Play with display off**: Verify understanding of video with only audio and descriptions