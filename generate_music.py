from audiocraft.models import MusicGen
import torchaudio
from datetime import datetime
import uuid
import os
import time

# Optional: output folder
os.makedirs("output", exist_ok=True)

# # Select instrument/style
# instruments = {
#     '1': 'violin solo',
#     '2': 'orchestral strings section',
#     '3': 'piano and strings',
#     '4': 'full orchestra',
#     '5': 'piano solo',
#     '6': 'cello solo',
#     '7': 'brass ensemble',
#     '8': 'woodwinds and strings',
#     '9': 'harp and strings'
# }

# # Print options
# print("\n🎻 Select instrument/style:")
# for key, value in instruments.items():
#     print(f"{key}: {value}")

# # Get user selection
# selection = input("\nEnter number (1-9): ")
# instrument = instruments.get(selection, 'orchestral strings section')  # default if invalid input

# # Define the musical style or emotion
# print("\n🎭 Enter the musical style or emotion (e.g., 'emotional', 'dramatic', 'peaceful'): ")
# style = input()

prompt2 = (
    "A grand symphonic journey, unfolding with the grace and elegance of a masterful sonata: "
    "Commence with a gentle adagio, where delicate strings and soft woodwinds whisper the dawn of creation, setting a serene and contemplative mood. "
    "As the piece progresses to the allegro, let the music swell with vibrant harmonies and spirited motifs, capturing the majesty and wonder of the heavens and earth taking form. "
    "At the heart of the composition, a vivacious allegretto emerges, with triumphant brass and resonant percussion, celebrating the divine artistry of creation. "
    "As the music approaches its denouement, transition into a tender and reflective andante, where a solo piano, accompanied by a gentle string ensemble, conveys the tranquility and order of the universe. "
    "Conclude with a peaceful coda, as the music gracefully fades into silence, leaving a lingering sense of awe and fulfillment. "
    "Inspired by the timeless beauty of the cosmos and the harmonious balance of nature, this piece is a testament to the enduring power of creation, rendered with clarity, elegance, and emotional depth."
)

prompt3 = (
    "An orchestral masterpiece that unfolds in three distinct movements: "
    "The first movement, 'Dawn of Creation,' begins with a gentle adagio, where delicate strings and soft woodwinds set a serene and contemplative mood. "
    "The second movement, 'Majestic Formation,' transitions into an allegro, with vibrant harmonies and spirited motifs capturing the majesty and wonder of the heavens and earth taking form. "
    "The final movement, 'Triumphant Celebration,' reaches a vivacious allegretto, with triumphant brass and resonant percussion celebrating the divine artistry of creation. "
    "Throughout the piece, the orchestra weaves a tapestry of sound, with each section contributing to the overall narrative. "
    "The music concludes with a peaceful coda, as the orchestra gracefully fades into silence, leaving a lingering sense of awe and fulfillment. "
    "Inspired by the timeless beauty of the cosmos and the harmonious balance of nature, this piece is a testament to the enduring power of creation, rendered with clarity, elegance, and emotional depth."
)

prompt4 = (
    "An orchestral masterpiece structured in three distinct movements: "
    "The first movement, 'Gentle Awakening,' begins softly and calmly, with delicate strings and subtle woodwinds creating a serene, peaceful atmosphere. "
    "Gradually, the music builds in intensity, seamlessly transitioning into the second movement, 'Rising Majesty,' where powerful brass, vibrant strings, and dynamic percussion escalate dramatically, reaching a powerful and emotional climax. "
    "The third movement, 'Tranquil Reflection,' gently resolves the tension, featuring soothing, lyrical flute melodies intertwined with soft strings and gentle harp arpeggios, evoking a sense of calm, peace, and renewal. "
    "The piece concludes gracefully, leaving listeners with a lingering sense of tranquility and emotional fulfillment. "
    "Inspired by the harmonious beauty of nature and the emotional journey of renewal and reflection, this composition is crafted with clarity, elegance, and expressive depth."
)

genesis0_1 = (
    "An orchestral masterpiece vividly depicting the creation narrative, structured meticulously: "
    "From 0 to 11 seconds, begin with near silence, a subtle, barely audible ambiance representing the void before creation. "
    "At 13 seconds, swiftly transition into a chaotic, fast-moving violin passage, symbolizing the divine spirit moving across the face of the waters. "
    "At 15 seconds, erupt into a brilliant explosion of sound with triumphant French horns and oboes, representing the sudden burst of divine light. "
    "From 17 to 40 seconds, introduce battling horns reminiscent of Wagner's 'Flight of the Valkyries,' capturing the intensity and drama of creation's early chaos. "
    "At 40 seconds, gently transition into calming violins and cellos, gradually bringing harmony and tranquility. "
    "At 1:05, introduce delicate harp melodies, symbolizing the emergence of form and order from chaos, progressively joined by harmonious strings. "
    "At 1:30, powerful, heroic horns reminiscent of Rossini's 'William Tell Overture' emerge, signifying strength and clarity. "
    "From 1:40 onwards, the music grows increasingly structured and orderly, echoing the majestic resolution of Tchaikovsky's '1812 Overture.' "
    "At 2:00, evoke the dramatic intensity of Mussorgsky's 'Night on Bald Mountain,' transitioning into a serene sunrise. "
    "At 2:10, introduce opposing bass drums, creating a brief tension before resolving into a gentle, harmonious orchestral ensemble at 2:25. "
    "From 2:25 to 4:50, the music becomes progressively calmer, more orderly, and quieter, with occasional subtle sounds of nature's harmony—birdsong, gentle breezes, and flowing water—reflecting the peaceful beauty of creation fully realized. "
    "This composition is deeply inspired by the profound imagery of creation, capturing the journey from chaos to divine order with emotional depth, clarity, and orchestral brilliance."
)

genesis1 = (
    "An orchestral masterpiece vividly depicting the creation narrative, structured meticulously: "
    "From 0 to 3 seconds, absolute silence, representing the profound void and nothingness before creation. "
    "At exactly 3 seconds, a sudden, powerful orchestral boom—an explosion of brilliant sound and light, symbolizing the divine spark of creation. "
    "Immediately following the explosion, from 4 seconds onward, a swift, intricate piano passage emerges, vividly portraying the divine spirit moving rapidly across the face of the waters, filled with urgency and purpose. "
    "At 13 seconds, swiftly transition into a chaotic, fast-moving violin passage, intensifying the sense of divine movement and energy. "
    "At 15 seconds, erupt into a brilliant explosion of sound with triumphant French horns and oboes, representing the sudden burst of divine illumination. "
    "From 17 to 40 seconds, introduce battling horns reminiscent of Wagner's 'Flight of the Valkyries,' capturing the intensity and drama of creation's early chaos. "
    "At 40 seconds, gently transition into calming violins and cellos, gradually bringing harmony and tranquility. "
    "At 1:05, introduce delicate harp melodies, symbolizing the emergence of form and order from chaos, progressively joined by harmonious strings. "
    "At 1:30, powerful, heroic horns reminiscent of Rossini's 'William Tell Overture' emerge, signifying strength and clarity. "
    "From 1:40 onwards, the music grows increasingly structured and orderly, echoing the majestic resolution of Tchaikovsky's '1812 Overture.' "
    "At 2:00, evoke the dramatic intensity of Mussorgsky's 'Night on Bald Mountain,' transitioning into a serene sunrise. "
    "At 2:10, introduce opposing bass drums, creating a brief tension before resolving into a gentle, harmonious orchestral ensemble at 2:25. "
    "From 2:25 to 4:50, the music becomes progressively calmer, more orderly, and quieter, with occasional subtle sounds of nature's harmony—birdsong, gentle breezes, and flowing water—reflecting the peaceful beauty of creation fully realized. "
    "This composition is deeply inspired by the profound imagery of creation, capturing the journey from chaos to divine order with emotional depth, clarity, and orchestral brilliance."
)

genesis2 = { 
    "Opening with a majestic orchestral introduction, featuring rich string ensemble harmonies and grand piano melodies painting an auditory landscape of Genesis 2's setting.",
    "Soft choir voices emerge, adding depth to the soundscape as the piece evolves.",
    "A dramatic crescendo symbolizing the creation of life unfolds, leading into a romantic era style interlude where leitmotifs subtly weave through expressive instrumental melodies.",
    "The music then transitions seamlessly into an epic, sweeping segment imbued with wonder and grandeur, evoking feelings of divine presence and majesty.",
    "A dramatic pause ensues before powerful brass tones entrance, emphasizing the importance of each creative act described in Genesis 2.",
    "The piece reaches a climactic peak, filled with intensity and emotion, representing the magnitude of God's work.",
    "Finally, the music resolves triumphantly, ethereal string ensemble tones gently guiding listeners to a serene conclusion.",
    "Atmospheric elements are interspersed throughout, enhancing the overall emotional journey, leaving the listener in a state of reverence and reflection on the beauty and complexity of creation."
}

genesis2_2 = {"Begin with an orchestral tapestry - rich strings, resonant piano, gentle winds and percussion painting the scene of Genesis 2.",
              " Introduce soft choir voices, adding a human touch to this symphonic journey. ",
              "A gradual crescendo swells, mirroring the birth of life as described in the verse, punctuated by a romantic era style interlude filled with expressive leitmotifs.",
"The piece then evolves into an epic, sweeping segment imbued with wonder and grandeur, evoking feelings of divine presence and majesty.", 
"A dramatic pause unfolds before powerful brass tones entrance, emphasizing the importance of each creative act in Genesis 2.",
" The music reaches a climactic peak filled with intensity and emotion, representing the magnitude of God's work.",
"As the piece resolves triumphantly, delicate string ensemble tones guide listeners to a serene conclusion, interspersed with atmospheric elements that enhance the overall emotional journey. ",
"This musical narrative leaves the listener in a state of reverence and reflection on the beauty and complexity of creation."
}

genesis2_3 = {
    "Commence with an ethereal orchestral introduction - soft strings, gentle piano, airy winds and subtle percussion setting the stage for Genesis 2's creation story.",
    "Introduce a celestial choir, adding a sense of divine presence to this tranquil symphonic journey.",
    "A serene crescendo blossoms as life emerges, mirroring the peaceful birth of the world.",
    "Transition into a tender interlude for Adam's tale of solitude - introspective piano melodies and poignant strings evoke feelings of longing and quiet reflection.", 
    "The music then swells with warmth and hope as Eve is created, marking the beginning of the first love story.",
    "A romantic era style segment unfolds, complete with expressive leitmotifs that weave through lush instrumental melodies.", 
    "Soft choir voices re-emerge, adding depth to this enchanting musical narrative.", 
    "The piece then evolves into an epic, sweeping segment imbued with wonder and majesty as the story reaches its emotional climax.",
    "Finally, the music resolves tenderly, delicate string ensemble tones guiding listeners to a serene conclusion filled with warmth and love.", 
    "Atmospheric elements are interspersed throughout, enhancing the overall emotional journey - leaving the listener in a state of wonder, joy and appreciation for the beauty and complexity of God's creation."
}

Genesis3 = {
    "Genesis Chapter 3, in 4 parts: the deception of the Serpent to Eve, The Fall of Adam to his wife, The Confrontation of God, The Fall from Grace",
"Part 1 - Orchestral, Symphonic, Dark and mysterious Grand Piano, Slow tempo, String Ensemble playing pensive notes, Choir whispering in hushed tones, Dramatic Crescendo during the serpent's deception, Majestic yet somber Romantic Era harmonies, Leitmotif for the serpent."
"Part 2 - Orchestral, Symphonic, Rich and full Grand Piano, Slow tempo, String Ensemble playing gentle harmonies, Choir singing softly with innocence, Gradual building Crescendo as Adam falls, Emotional depth showcasing the consequences."
"Part 3 - Orchestral, Symphonic, Majestic and regal Grand Piano, Moderate tempo, String Ensemble playing powerful harmonies, Choir singing in awe during confrontation, Dramatic tension in the orchestration."
"Part 4 - Orchestral, Symphonic, Epic and Sweeping score, Slow tempo, String Ensemble playing poignant notes, Choir whispering with sorrow, Intense moments mirroring internal turmoil, Triumphant resolution hinting at redemption, Ethereal textures evoking a sense of wonder, Atmospheric elements underscoring the feeling of change, Grandiose finale encapsulating the magnitude of the story."
}
AugustusComposer = {
    "Music that describes God moving over the face of the waters in Genesis would be a composition that captures a sense of divine presence and power. It would start with a gentle, flowing melody to represent the calmness of the waters before God's movement."
    "As the music progresses, it would build in intensity and grandeur, symbolizing the stirring of the waters as God's presence hovers over them. The use of deep, resonant tones and soaring melodies would evoke a sense of awe and majesty, reflecting the profound impact of God's presence on the waters."
    "The music would convey a mix of tranquility and power, mirroring the imagery of God's creative spirit moving over the face of the deep in Genesis."
    " In this excerpt from *De Musica*, I explain how music can be crafted to evoke the imagery of God moving over the face of the waters in Genesis. The composition is described as starting with a gentle and flowing melody to portray the initial calmness of the waters before God's action." 
    "This serene beginning sets the stage for the unfolding of divine power and presence. As the music progresses, it intensifies in both tone and grandeur to symbolize the stirring of the waters as God's mighty presence hovers over them. The gradual buildup in the composition mirrors the transformative and awe-inspiring nature of God's creative act." 
    "Deep, resonant tones are used alongside soaring melodies to convey a sense of majesty and reverence befitting the image of God's spirit moving over the deep waters. Overall, the music described in this passage aims to combine elements of peace and power, tranquility and majesty, to reflect the profound mystery and grandeur of God's presence and creative work as depicted in the book of Genesis."
    }
# Combine into a detailed prompt
prompt = f"A cinematic orchestral piece. {AugustusComposer}"

print(f"\n🎼 Generated prompt:\n{prompt}\n")

# Generate music using MusicGen
model = MusicGen.get_pretrained('medium')
model.set_generation_params(duration=175)  # 60 seconds
# Start music generation
start_time = time.time()
start_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(f"🎶 Starting music generation at {start_timestamp}")
print("This may take several minutes...")


wav = model.generate([prompt])


# Calculate duration
end_time = time.time()
duration_seconds = end_time - start_time
minutes, seconds = divmod(duration_seconds, 60)

# Save the audio file
filename = f"output/{datetime.now().strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:8]}.wav"
torchaudio.save(filename, wav[0].cpu(), sample_rate=32000)
# Final output with timestamp and duration
end_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(f"✅ Music generation completed at {end_timestamp}")
print(f"⏱️ Total generation time: {int(minutes)} minutes and {int(seconds)} seconds")
print(f"🎵 Music saved to: {filename}")