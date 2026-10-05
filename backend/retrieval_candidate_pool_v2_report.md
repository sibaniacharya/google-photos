# Retrieval Candidate Pool v2 Report

1. **Total input records:** 2022
2. **Number of incomplete-memory candidates:** 3
3. **Number of successful-retrieval candidates:** 0
4. **Number of records excluded:** 2019
5. **Signal distribution for excluded:**
   - Retrieval Intent Only (A): 79
   - Memory Ambiguity Only (B): 20
   - Neither: 1920

## 6. 20 Strongest Candidates

### 1. [INCOMPLETE_MEMORY_CANDIDATE] ID: ff568fd2
- **Matched Retrieval Signals:** (?:find|locate|search for|look(?:ing)? for|retrieve)\s+(?:a|an|the|that|my|old|particular|specific|certain)?\s*(?:photo|picture|image|video|pic)
- **Matched Memory Signals:** forgot
- **Original Quote:**
  > I love how it makes videos from all the old pictures I had forgotten about and helps me find pictures of people

### 2. [INCOMPLETE_MEMORY_CANDIDATE] ID: 63d16073
- **Matched Retrieval Signals:** (?:find|locate|search for|look(?:ing)? for|retrieve)\s+(?:a|an|the|that|my|old|particular|specific|certain)?\s*(?:photo|picture|image|video|pic)
- **Matched Memory Signals:** forgot
- **Original Quote:**
  > back and they find the photos that things that you have actually forgotten about got to try something

### 3. [INCOMPLETE_MEMORY_CANDIDATE] ID: d2066701
- **Matched Retrieval Signals:** (?:find|locate|search for|look(?:ing)? for|retrieve)\s+(?:a|an|the|that|my|old|particular|specific|certain)?\s*(?:photo|picture|image|video|pic)
- **Matched Memory Signals:** vague
- **Original Quote:**
  > Baffling UI choices continue. Want to easily find a photo from a certain date using easy visuals? Tough. It's now a homogeneous mess that just dumps all your photos together with no separation. It gives a vague date at the top, but you might have three photos in a row from two different days. Don't worry, that doesn't matter because now photos uses ✨AI✨ because of course it does.

## 7. Examples of obvious false positives excluded by the 2-signal rule

These reviews contain isolated words like 'find', 'old', or 'remember', but do not represent the target retrieval problem.

**False Positive 1:**
> Whoever designed this was linguistically challenged. Stop using so many synonyms. Images, photos, pictures, is all the SAME thing!!! If there's a way to be ignorant, people will find it. You star a photo and can't find it elsewhere. It gets filed under collections that doesn't show up everywhere either. Then you run into a stupid folder called favorites. Starred and favorites is the SAME thing. This is a display of massive lack of intelligence.

**False Positive 2:**
> Google Photos is a convenient and reliable app for storing, organizing, and managing photos and videos. I really like the automatic backup, smart search, albums, and easy sharing features. The ability to search for specific people, places, or things makes finding old photos much easier. I also enjoy the editing tools, memories, and helpful suggestions for creating collages and other photo creations. Overall, Google Photos makes it easy to keep precious memories organized and backed up.

**False Positive 3:**
> Not intuitive for digital art, which most of my pictures are. The Memories and Face Recognition and such only pay attention to the (very few) actual photos and thus are not helpful. AI tools are trash. If this app wasn't conveniently synced to my Google account I would uninstall and find something else. Also, make the "folders" button easier to get to, and then STOP MOVING IT AROUND! And stop rearranging the order of the *comic panels* in my *album*.

**False Positive 4:**
> The interface is so nice and clean! Old photos are easy to find and the albums are very organized

**False Positive 5:**
> MY PHOTOS ARE MISSING!!!! My old photos that were backed up and I could see earlier are missing now. I was deleting some of the old photos and realised a huge chunk of my old photos are missing. I don't know how to find them, there were some important, memorable photos in there and now they're gone. What am I supposed to do now? I want my old photos back.

