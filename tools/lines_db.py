BUDDY_SAYS = {
    'keytar': ['TOTALLY RADICAL!', 'SYNTH ATTACK!', 'NEON POWER!', 'KEYTAR TIME!', 'FEEL THE SYNTH!', 'BACK TO THE 80S!'],
    'biker': ['OUTTA MY WAY!', 'BORN TO RIDE!', 'HIGHWAY STAR!', 'FULL THROTTLE!', 'HOLD MY HELMET!', 'BRAKES ARE FOR WIMPS!'],
    'boar': ['FOR THE FORGE!', 'OINK OF DOOM!', 'THE KING CHARGES!', 'SNOUT FIRST!', 'HOG RUSH!', 'ALL HAIL THE HOG!'],
    'reaper': ['YOUR TIME IS UP.', 'THE END IS NEAR.', 'I COME FOR YOU.', 'SCYTHE TIME.', 'REST IN PIECES.', 'TICK TOCK.'],
    'dj': ['DROP THE BASS!', 'DJ IN THE HOUSE!', 'TURN IT UP!', 'BASS CANNON!', 'HANDS IN THE AIR!', 'WUB WUB TIME!'],
}

CH = {}
CH[1] = dict(
    lines={'start': ["Let's roll!", 'Skates on, let us go!', 'Time to glide!', 'Neon City, here I come!', 'Watch me shine!', 'Rolling out!'],
           'low': ['Come on, come on!', 'Focus, girl!', 'Do not lose it now!', 'Stay in the groove!', 'I can still do this!'],
           'recover': ['Back in the groove!', 'That is more like it!', 'Feeling it again!', 'Smooth sailing!', 'Here we go again!'],
           'combo': ['Totally tubular!', 'Radical!', 'So rad!', 'Like, wow!', 'Gnarly streak!'],
           'mini': ['Yeah! Take that!', 'Box that up!', 'Volume down, loser!', 'Nailed it!', 'Booyah!'],
           'boss': ['Neon City is free!', 'Game over, Mainframe!', 'Unplugged for good!', 'The city glows again!', 'System shut down!'],
           'fixed': ['']},
    rival={'start': ['Try to keep up!', 'Out of my way, rookie!', 'This street is mine!', 'Bet you cannot catch me!', 'Ready to lose?'],
           'win': ['Too slow!', 'Better luck next time!', 'Eat my sparkles!', 'Is that all?', 'Bye bye, slowpoke!'],
           'kick': ['Take that!', 'Hi-yah!', 'Skate kick!', 'Gotcha!', 'Boom!'],
           'hurt': ['Ow! No fair!', 'My skates!', 'Hey! Rude!', 'Ouch, okay, okay!', 'You will pay for that!'],
           'taunts': ['NICE SKATES, GRANDMA!', 'IS THAT A WALKMAN? CUTE.', 'I SKATE BLINDFOLDED!', 'YOUR HAIR IS SO LAST YEAR', 'PINK IS MY COLOR, NOT YOURS']},
    boss={'enter': ['Your rhythm is obsolete.', 'Initiating meltdown.', 'Welcome to my circuit.', 'Prepare for deletion.', 'I am the music now.'],
          'rev': ['Error. Fun not found.', 'Your keys are mine.', 'Input scrambled.', 'Confusion protocol online.', 'Reverse polarity!'],
          'cor': ['Deleting your groove.', 'Space bar corrupted.', 'Formatting your fun.', 'Your space is gone.', 'Virus uploaded.'],
          'fin': ['I. Cannot. Compute.', 'System failure imminent.', 'Critical error!', 'Rebooting. No!', 'Abort! Abort!'],
          'ko': ['Noooo!', 'Blue screen of death!', 'Shutting. Down.', 'Fatal exception!', 'Goodbye, world!']},
    duet={'line': ["Let's jam!", 'Rock and roll!', 'Need a guitar?', 'Duet time!', 'Crank it up!'],
          'atkLine': ['GUITAR TOSS!', 'CATCH THIS!', 'INCOMING AXE!', 'HEADS UP!', 'FLYING V!'], 'atkWord': ['BONK!', 'KLONK!', 'TWANG!', 'THWACK!', 'CLANG!'],
          'healLine': ['HAVE A PICK!', 'LUCKY PICK!', 'TAKE A BREATHER!', 'ROCK ON!', 'HERE, CATCH!'],
          'healReact': ['THANKS, DUDE!', 'RADICAL!', 'SWEET!', 'I OWE YOU!', 'TUBULAR!'], 'healWord': ['CATCH!', 'YOINK!', 'GOT IT!', 'NICE!', 'SNAG!']})
CH[2] = dict(
    lines={'start': ["Let's rock!", 'Highway to rock!', 'Turn it up!', 'Ready to shred!', 'Road trip, baby!'],
           'low': ['Stay in tune!', 'Do not choke now!', 'Keep the rhythm!', 'Focus on the riff!', 'Come on, rock it!'],
           'recover': ['Back on the road!', 'Now we are rolling!', 'That is the stuff!', 'Back in tune!', 'Feel that groove!'],
           'combo': ['Rock and roll!', 'Shred it!', 'Face melted!', 'Heck yeah!', 'Riff city!'],
           'mini': ['Unplugged!', 'Wall torn down!', 'Volume zero!', 'Smashed it!', 'Encore for me!'],
           'boss': ['The highway is ours!', 'Titan unplugged!', 'Rock never dies!', 'That is a wrap!', 'Sold out show!'],
           'fixed': ['Good as new! Let us rock!', 'Strings are back!', 'Guitar fixed, let us go!', 'Back in business!', 'Time to shred again!']},
    rival={'start': ['Eat my dust!', 'Hit the road, roadie!', 'My amp is louder!', 'This gig is mine!', 'You call that a riff?'],
           'win': ['Too slow, roadie!', 'Encore for me!', 'Better luck next tour!', 'You got outplayed!', 'Go home, garage band!'],
           'kick': ['Eat this!', 'Power kick!', 'Stage dive!', 'Rock out!', 'Boot to the face!'],
           'hurt': ['My solo!', 'My hair!', 'Not the guitar!', 'Ouch! Cheap shot!', 'Hey, my amp!'],
           'taunts': ['MY AMP IS BIGGER!', 'YOU PLAY LIKE A KAZOO!', 'NICE HAIR. NOT.', 'I TUNED MY GUITAR, YOU?', 'ROADIES DONT GET SOLOS']},
    boss={'enter': ['Prepare for maximum volume!', 'Feel the feedback!', 'Turn it up to eleven!', 'I am the loudest!', 'Your ears are mine!'],
          'broken': ['Your guitar is mine!', 'Snap goes the string!', 'No more solos!', 'Shred this!', 'Unplug the hero!'],
          'fin': ['Turn it down! Turn it down!', 'My speakers!', 'Too much gain!', 'Feedback overload!', 'Not the subwoofers!'],
          'ko': ['Feedback overload!', 'Blown speakers!', 'Static. Static.', 'I am unplugged!', 'Turn me off!']},
    duet={'line': ['For the forge!', 'Hammer time!', 'Dwarves rock too!', 'Let us smash!', 'To battle, lad!'],
          'atkLine': ['ALE INCOMING!', 'CATCH, BEASTIE!', 'MUG MISSILE!', 'BOTTOMS UP!', 'TAKE A DRINK!'], 'atkWord': ['SPLOSH!', 'SPLASH!', 'GLUG!', 'SPLAT!', 'KER-SPLOOSH!'],
          'healLine': ['HAVE A SIP!', 'DRINK UP, LAD!', 'A TOAST TO YOU!', 'ALE HEALS ALL!', 'ONE FOR YOU!'],
          'healReact': ['HIC!', 'BURP!', 'STRONG STUFF!', 'WHOA, SPICY!', 'HIC! THANKS!'], 'healWord': ['CHUG!', 'GULP!', 'SLURP!', 'SKAL!', 'GLUG GLUG!']},
    helper=['Need a hand, rocker?', 'Neon skater to the rescue!', 'Let me show you how!', 'Skate break, rocker!', 'I got this, rock star!'])
CH[3] = dict(
    lines={'start': ['For the forge!', 'Steel and stone!', 'Let the hammer sing!', 'To battle!', 'Dwarves never quit!'],
           'low': ['Hold the line!', 'Stand firm!', 'Not today!', 'Steady, steady!', 'Grit your teeth!'],
           'recover': ['Steel yourself!', 'The forge burns again!', 'That is the spirit!', 'Back to the anvil!', 'Mighty!'],
           'combo': ['Hammer time!', 'Strike while it is hot!', 'By my beard!', 'Unbreakable!', 'Forged in fire!'],
           'mini': ['The troll is down!', 'Drum solo over!', 'Smashed like ore!', 'Back to your cave!', 'Timber!'],
           'boss': ['The forge is saved!', 'Dragon slain!', 'The keep is ours!', 'Ale for everyone!', 'Victory, brothers!'], 'fixed': ['']},
    rival={'start': ['My beard is longer!', 'Out of my mine!', 'I forge faster!', 'Your hammer is a toothpick!', 'Step aside, pebble!'],
           'win': ['Ha! Beardless whelp!', 'Back to the mines!', 'I win, shorty!', 'Better luck next century!', 'My ale now!'],
           'kick': ['Headbutt!', 'Beard slap!', 'Iron boot!', 'Hammer smash!', 'Dwarf toss!'],
           'hurt': ['My beard!', 'My helmet!', 'Ow, my toes!', 'Not the beard!', 'You will pay, stone face!'],
           'taunts': ['MY BEARD IS BRAIDED!', 'YOUR HAMMER IS RUSTY!', 'I DRINK TWICE YOUR ALE!', 'YOUR HELMET IS DENTED', 'I MINED MORE GOLD THAN YOU']},
    boss={'enter': ['Your forge will melt!', 'I smell dwarf!', 'Burn, little one!', 'The keep is mine!', 'Feel the magma!'],
          'rev': ['Your mind is mine!', 'Confusion burns!', 'Left is right now!', 'Dance, little dwarf!', 'Twisted by flame!'],
          'cor': ['Your space is ash!', 'Ashes to ashes!', 'Burnt to a crisp!', 'No space for you!', 'Smoke and cinders!'],
          'fin': ['My scales are cracking!', 'Impossible!', 'My fire fades!', 'Mercy!', 'Not my hoard!'],
          'ko': ['Roooaaar!', 'My gold!', 'Extinguished!', 'The flame dies!', 'Defeated by a dwarf!']},
    duet={'line': ['Let the darkness play.', 'The night is ours.', 'Shadows, rise.', 'I bring the gloom.', 'A dark duet, then.'],
          'atkLine': ['GO, MY CROW!', 'PECK THEM!', 'FLY, MY DARLING!', 'CROW STRIKE!', 'CAW CAW, ATTACK!'], 'atkWord': ['PECK PECK!', 'CAW!', 'SCRATCH!', 'PECKITY!', 'KRAAAW!'],
          'healLine': ['A POEM FOR YOU...', 'LISTEN TO THE NIGHT', 'DARKNESS HEALS...', 'A SAD SONG, FOR YOU', 'THE MOON BLESSES YOU'],
          'healReact': ['...SO DEEP.', '...WOW. DARK.', '...SAD BUT GOOD', '...MORE POETRY?', '...NEEDED THAT.'], 'healWord': ['SIGH...', 'SNIFF...', 'SO MOVING...', 'AWW...', 'GLOOM UP!']})
CH[4] = dict(
    lines={'start': ['Let the night begin.', 'Into the darkness.', 'The moon is watching.', 'Ravenmoor awaits.', 'Shadows, follow me.'],
           'low': ['The night grows cold.', 'Do not falter.', 'Darkness, guide me.', 'Not like this.', 'Stay with me, crow.'],
           'recover': ['The night embraces me.', 'Back from the abyss.', 'Gloriously gloomy.', 'The shadows return.', 'Better. Darker.'],
           'combo': ['Exquisitely dark!', 'Gothic perfection!', 'The bats approve!', 'Hauntingly good!', 'Dreadfully divine!'],
           'mini': ['Back to stone.', 'Crumble, gargoyle.', 'Rest in pieces.', 'Stony silence.', 'Gargoyle grounded.'],
           'boss': ['The Countess falls.', 'Ravenmoor is free.', 'Dawn breaks at last.', 'No more bloodsucking.', 'The night is mine.'],
           'fixed': ['The trance is broken.', 'My mind is my own.', 'Thank you, little dwarf.', 'Back to the shadows.', 'The gloom returns.']},
    rival={'start': ['My eyeliner is darker!', 'You call that gloomy?', 'Ravenmoor is mine!', 'Sulk faster!', 'The night prefers me!'],
           'win': ['Too bright, too slow!', 'Embrace defeat!', 'Back to your coffin!', 'So sad, for you!', 'Darkness wins!'],
           'kick': ['Gloom kick!', 'Feel my despair!', 'Shadow strike!', 'Kneel!', 'Taste the night!'],
           'hurt': ['My cape!', 'My eyeliner!', 'You ruined my gloom!', 'Ow, how tragic!', 'My poetry!'],
           'taunts': ['MY EYELINER IS DARKER', 'YOUR CROW IS A PIGEON', 'I WAS SAD FIRST', 'NICE CAPE. FROM A STORE?', 'I LISTEN TO WORSE MUSIC'],
           'yoink': ['Into the shadows!', 'Lost in the fog?', 'Wrong grave!', 'Spooky, right?', 'Boo! Moved them!'],
           'snatch': ['Your friend is mine!', 'I collect souls!', 'Gloomy thanks!', 'Darkness takes it!', 'Mine, forever!']},
    boss={'enter': ['Welcome to my ball.', 'Such a pretty neck.', 'Dance with me, darling.', 'The night belongs to me.', 'Just in time for dinner.'],
          'rev': ['Look into my eyes.', 'Your hands obey me.', 'Mesmerized, darling?', 'Dance backwards for me.', 'Hypnosis!'],
          'fin': ['My beauty, fading!', 'The sun? No!', 'Impossible, mortal!', 'My castle!', 'Spare me, darling!'],
          'ko': ['Aaargh! The dawn!', 'Curse you!', 'My eternal night!', 'Turned to dust!', 'Not my lovely face!']},
    duet={'line': ['Yo, let me drop in!', 'Mic check, one two!', 'I got your back, goth!', 'Let us remix this!', 'Beat on, darkness!'],
          'atkLine': ['VINYL FRISBEE!', 'SPIN THAT!', 'CATCH THIS RECORD!', 'SCRATCH THAT!', 'DISC INCOMING!'], 'atkWord': ['SCRATCH!', 'WICKA!', 'THWIP!', 'SPLAT!', 'ZZZIP!'],
          'healLine': ['YOU GOT THIS!', 'HYPE MODE ON!', 'HANDS UP, GOTH!', 'KEEP IT REAL!', 'STAY HYPED!'],
          'healReact': ['...YEAH?', '...HYPED. IN BLACK.', '...I FEEL GOOD. UGH.', '...DARKLY HYPED.', '...OKAY THAT HELPED'], 'healWord': ['HYPE!', 'YEAH!', 'WORD!', 'HOLLA!', 'UP UP!']},
    helper=['Stand back, lad!', 'Dwarf to the rescue!', 'Let me hammer this!', 'Hold my ale!', 'Metal time, goth!'])
CH[5] = dict(
    lines={'start': ['Mic check, one two!', 'Let me drop this!', 'Yo, let us go!', 'Concrete jungle, here I come!', 'Beat drop, I am up!'],
           'low': ['Keep the flow!', 'Stay on beat!', 'Breathe, focus!', 'Do not choke now!', 'Find the rhythm!'],
           'recover': ['Back on the beat!', 'Flow restored!', 'Now we talking!', 'That is the vibe!', 'Locked in!'],
           'combo': ['Straight fire!', 'On beat, all day!', 'Bars on bars!', 'Flow is crazy!', 'Too smooth!'],
           'mini': ['Painted over!', 'Erased!', 'Tag, you are it!', 'Golem got cleaned!', 'Wall is wiped!'],
           'boss': ['Pitch corrected!', 'Concrete City is free!', 'Mic drop!', 'Real voices win!', 'Autotune is done!'],
           'fixed': ['Mic is back!', 'Unjammed, let us go!', 'Voice is back!', 'Mic restored, yo!', 'Back on the mic!']},
    rival={'start': ['You call that flow?', 'This block is mine!', 'I spit hotter bars!', 'Step aside, amateur!', 'Ready for a battle?'],
           'win': ['Too slow on the beat!', 'I won the battle!', 'Weak bars, kid!', 'Go home, rookie!', 'Mic belongs to me!'],
           'kick': ['Diss track!', 'Bar slam!', 'Freestyle kick!', 'Take this verse!', 'Mic smack!'],
           'hurt': ['My chain!', 'My kicks!', 'Not the cap!', 'Ow, foul!', 'You messed up my flow!'],
           'taunts': ['YOUR RHYMES ARE MID', 'MY CAP FACES FORWARD', 'NICE TANK TOP, GRANDPA', 'I GOT MORE FOLLOWERS', 'YOU RAP LIKE A TOASTER'],
           'yoink': ['Remixed your lanes!', 'Scratch that!', 'Flipped the beat!', 'Off beat now!', 'Wrong track, kid!'],
           'snatch': ['Thanks for the hype!', 'Your DJ works for me!', 'Sampled your meter!', 'That is mine now!', 'Gimme that!']},
    boss={'enter': ['Your voice is off key.', 'Let me correct you.', 'Prepare to be tuned.', 'Natural voices are obsolete.', 'I am perfect pitch.'],
          'broken': ['Your mic is jammed!', 'Feedback loop!', 'Mic muted!', 'No voice for you!', 'Silence, mortal!'],
          'cor': ['Space? Deleted.', 'Your beat is corrupted.', 'Glitch the bass!', 'Error in the drop!', 'Your space is off beat!'],
          'fin': ['Pitch error!', 'Too much bass!', 'I am out of tune!', 'My algorithm!', 'Unquantized!'],
          'ko': ['Off. Key.', 'Pitch shift down!', 'Fatal flat note!', 'I was perfect!', 'Bzzzt, noooo!']},
    duet={'line': ['For glory and power!', 'Epic duet, my friend!', 'Let the dragons fly!', 'Steel and bars!', 'Unleash the power!'],
          'atkLine': ['POWER STAR!', 'FOR GLORY!', 'STAR OF STEEL!', 'EPIC THROW!', 'DRAGON STAR!'], 'atkWord': ['EPIC!', 'GLORY!', 'VALOR!', 'SHING!', 'HUZZAH!'],
          'healLine': ['A HEROIC SPEECH!', 'STAND TALL, BARD!', 'FEEL THE POWER!', 'FOR HONOR!', 'BELIEVE!'],
          'healReact': ['...THAT WAS EPIC.', '...I FEEL HEROIC.', '...OKAY, BET.', '...WORD.', '...FIRED UP!'], 'healWord': ['HUZZAH!', 'VALOR!', 'GLORY!', 'HONOR!', 'EPIC!']})


def apply(chapter, n):
    d = CH[n]
    chapter['lines'] = d['lines']
    chapter['rivalLines'].update(d['rival'])
    keep = {k: v for k, v in chapter['bossLines'].items() if k == 'taunts'}
    chapter['bossLines'] = dict(d['boss'], **keep)
    for k in ('enter', 'rev', 'cor', 'broken', 'fin'):
        if k in d['boss']:
            fits = [v for v in d['boss'][k] if len(v) <= 22]
            chapter['bossLines'][k + 'Txt'] = (fits[0] if fits else d['boss'][k][0][:22]).upper()
    chapter['duet'].update(d['duet'])
    if 'helper' in d and chapter.get('helper'):
        chapter['helper']['line'] = d['helper']
    b = chapter['buddy']
    b['says'] = BUDDY_SAYS[b['sfx']]

BUDDY_SAYS['headbang'] = ['HEADBANG!!!', 'NECKS OF STEEL!', 'HAIR OF FURY!', 'MOSH PIT ASSEMBLE!', 'WINDMILL TIME!', 'FOR THE HORDE!']
CH[6] = dict(
    lines={'start': ['For glory!', 'To the citadel!', 'Steel and thunder!', 'Ride the wind!', 'The sky awaits!'],
           'low': ['Hold fast!', 'Do not yield!', 'Courage, bard!', 'Stand tall!', 'The legend is not over!'],
           'recover': ['Glory returns!', 'Back in the saga!', 'The power flows!', 'Onward!', 'Heroic!'],
           'combo': ['Epic!', 'Legendary riff!', 'For the kingdom!', 'Unstoppable steel!', 'Power overwhelming!'],
           'mini': ['The bull is beaten!', 'Labyrinth conquered!', 'Horns down!', 'Moo no more!', 'Victory in the maze!'],
           'boss': ['The storm is broken!', 'The sky is free!', 'Thunder falls silent!', 'A legend is born!', 'Glory forever!'],
           'fixed': ['I rise again!', 'The bard returns!', 'My strength is back!', 'Thank you, friend!', 'Back to glory!']},
    rival={'start': ['My hair flows better!', 'The ballads are mine!', 'Kneel, minstrel!', 'This saga is mine!', 'My solo is longer!'],
           'win': ['Victory is mine!', 'Bow to the true bard!', 'Your legend ends!', 'Too slow, squire!', 'Glory to me!'],
           'kick': ['Sword kick!', 'Hair whip!', 'Shield bash!', 'For my glory!', 'Feel my valor!'],
           'hurt': ['My hair!', 'My cape!', 'Not the guitar!', 'You cad!', 'This is not over!'],
           'taunts': ['MY HAIR IS SILKIER', 'I KNOW 400 BALLADS', 'YOUR CAPE IS SMALL', 'DRAGONS FEAR ME, NOT YOU', 'I HIT HIGHER NOTES']},
    boss={'enter': ['I am the storm!', 'Kneel before thunder!', 'The sky is mine!', 'Feel the tempest!', 'Lightning obeys me!'],
          'cor': ['Thunder takes your space!', 'Space shattered!', 'The storm devours!', 'Your space is lightning!', 'Crackle and burn!'],
          'fin': ['My clouds are breaking!', 'Impossible!', 'The sun? No!', 'My thunder fades!', 'Mercy, hero!'],
          'ko': ['Kaboooom!', 'My storm!', 'Clear skies? Never!', 'I am drizzle now!', 'Noooo!']},
    duet={'line': [''], 'atkLine': [''], 'atkWord': [''], 'healLine': [''], 'healReact': [''], 'healWord': ['']})

BUDDY_SAYS['bigband'] = ['SWING IT!', 'HIT IT, BOYS!', 'A-ONE, A-TWO!', 'BRASS SECTION, GO!', 'BIG BAND, BIG SOUND!', 'TAKE IT AWAY!']
CH[7] = dict(
    lines={'start': ['Let us swing, baby!', 'Hit it!', 'Time to blow!', 'Dig this groove!', 'Smooth like butter!'],
           'low': ['Keep it cool, cat.', 'Easy, daddy-o.', 'Find the pocket.', 'Stay smooth.', 'Do not lose the swing!'],
           'recover': ['Back in the pocket!', 'Now we are cooking!', 'That is the swing!', 'Smooth again!', 'Groovy, baby!'],
           'combo': ['Hot jazz!', 'Cooking now!', 'Swinging!', 'Crazy cool!', 'Dig it!'],
           'mini': ['Bounced the bouncer!', 'Out you go!', 'Swing and a knockout!', 'Doors are open!', 'He got the blues!'],
           'boss': ['The city swings free!', 'Big Tony is busted!', 'Jazz is free!', 'Case closed, baby!', 'That is how we swing!'],
           'fixed': ['My sax is back!', 'Back in tune, baby!', 'Let us blow again!', 'Got my horn!', 'Swing time again!']},
    rival={'start': ['My trombone is louder!', 'Out of my club, kitty!', 'This alley is mine!', 'You call that swing?', 'Scat, cat!'],
           'win': ['Too square, daddy-o!', 'I swing harder!', 'Back to the alley!', 'Off the beat, kitty!', 'Bye bye, birdie!'],
           'kick': ['Trombone slide!', 'Tail pull!', 'Hat trick!', 'Scat attack!', 'Swing kick!'],
           'hurt': ['My whiskers!', 'My hat!', 'Not the trombone!', 'Hiss!', 'That is not cool!'],
           'taunts': ['YOUR SAX IS DENTED', 'I HAVE NINE LIVES LEFT', 'NICE HAT, GRANDPA', 'YOU PLAY LIKE A KAZOO', 'MY TAIL SWINGS BETTER']},
    boss={'enter': ['Nobody swings in my town!', 'This club is mine, kitty.', 'Pay up, or play out.', 'Welcome to the family.', 'You got some nerve, cat.'],
          'rev': ['Let me rearrange your fingers.', 'Play it backwards, kid!', 'Confused, kitty?', 'Wrong notes, wrong town!', 'Turn it around!'],
          'broken': ['I will take that sax!', 'Your horn is mine!', 'No more solos for you!', 'Confiscated!', 'That sax pays my debts!'],
          'fin': ['The coppers are coming!', 'My empire!', 'Not the trombone!', 'Have mercy, kitty!', 'I will make you an offer!'],
          'ko': ['I am busted!', 'Fuhgeddaboudit!', 'My casino!', 'Curse you, cat!', 'This is not the end!']},
    duet={'line': [''], 'atkLine': [''], 'atkWord': [''], 'healLine': [''], 'healReact': [''], 'healWord': ['']})

BUDDY_SAYS['stampede'] = ['YEEHAW!', 'STAMPEDE!', 'GIT ALONG, LITTLE DOGIES!', 'MOOOOVE IT!', 'HOLD YER HATS!', 'RIDE EM, COWBOY!']
CH[8] = dict(
    lines={'start': ['Yeehaw, let us ride!', 'Saddle up!', 'Time to pick some banjo!', 'Howdy, Dusty Gulch!', 'Let us kick up some dust!'],
           'low': ['Hold your horses!', 'Easy now, partner.', 'Steady in the saddle!', 'Do not get bucked off!', 'Keep picking, girl!'],
           'recover': ['Back in the saddle!', 'That is more like it!', 'Yee-haw, here we go!', 'Smooth riding now!', 'Picking up speed!'],
           'combo': ['Yeehaw!', 'Hot dang!', 'Pickin and grinnin!', 'Giddy up!', 'Rootin tootin!'],
           'mini': ['Tumbled it!', 'Weed whacked!', 'Roll on out!', 'Dust in the wind!', 'That weed is done!'],
           'boss': ['The train is derailed!', 'End of the line!', 'Dusty Gulch is free!', 'Iron Horse is scrap!', 'Yeehaw, we did it!'], 'fixed': ['']},
    rival={'start': ['This here is my town!', 'Draw, pardner!', 'My banjo is faster!', 'Ride on, greenhorn!', 'Ready to eat dust?'],
           'win': ['Too slow, greenhorn!', 'Fastest picker in the west!', 'Back to the ranch!', 'Yer done, pardner!', 'Eat my dust!'],
           'kick': ['Lasso!', 'Boot scoot!', 'Spur kick!', 'Yeehaw kick!', 'Rodeo slam!'],
           'hurt': ['My hat!', 'My spurs!', 'Dang it!', 'Not the banjo!', 'Ow, ya varmint!'],
           'taunts': ['YER BANJO IS OUT OF TUNE', 'MY HAT IS BIGGER', 'NICE BOOTS. FOR A CITY GAL', 'I RODE A BULL ONCE', 'YOU PICK LIKE A CHICKEN']},
    boss={'enter': ['All aboard the doom train!', 'Choo choo, you are through!', 'Next stop: your defeat!', 'Full steam ahead!', 'This is my railroad!'],
          'broken': ['I will snap those strings!', 'No more banjo for you!', 'Strings snapped!', 'Silence that banjo!', 'Twang no more!'],
          'cor': ['Your space is derailed!', 'Off the rails!', 'Space jam on the tracks!', 'Derail that drop!', 'Loose bolts, loose space!'],
          'fin': ['My boiler is bursting!', 'Too much steam!', 'Brakes! Brakes!', 'My wheels!', 'Not the caboose!'],
          'ko': ['Chooo... nooo!', 'Derailed!', 'Scrap metal!', 'Out of steam!', 'End of the line!']},
    duet={'line': [''], 'atkLine': [''], 'atkWord': [''], 'healLine': [''], 'healReact': [''], 'healWord': ['']})

BUDDY_SAYS['basscannon'] = ['BASS CANNON, FIRE!', 'DROP THE BEAM!', 'MAXIMUM WUB!', 'CHARGING SUBWOOFERS!', 'FEEL THE BASS!', 'WOBBLE TIME!']
CH[9] = dict(
    lines={'start': ['System online. Let us drop!', 'Bass mode: activated!', 'Plug in, power up!', 'Ready to rave!', 'Launching the beat!'],
           'low': ['Signal weak!', 'Recalibrate!', 'Do not lose sync!', 'Hold the frequency!', 'Stay on the grid!'],
           'recover': ['Sync restored!', 'Back on the grid!', 'Frequency locked!', 'Full power!', 'Bass is back!'],
           'combo': ['Wub wub!', 'Max frequency!', 'Drop it!', 'Overdrive!', 'Bass boosted!'],
           'mini': ['Bot unplugged!', 'Wobble deleted!', 'Error, bot!', 'Short circuit!', 'Powered down!'],
           'boss': ['The Drop is dropped!', 'Bass Planet is free!', 'Sound system restored!', 'Signal clear!', 'Game over, Drop!'], 'fixed': ['']},
    rival={'start': ['My drops are bigger!', 'This rave is mine!', 'You call that bass?', 'Out of my frequency!', 'Ready to get remixed?'],
           'win': ['Too slow, noob!', 'Drop denied!', 'Lag much?', 'Back to the tutorial!', 'You got remixed!'],
           'kick': ['Glitch kick!', 'Bass punch!', 'Laser kick!', 'Ctrl Alt Kick!', 'Hard reset!'],
           'hurt': ['My visor!', 'Lag spike!', 'Unfair!', 'My headphones!', 'Connection lost!'],
           'taunts': ['YOUR BPM IS TOO LOW', 'NICE VISOR. FROM 2010?', 'I HAVE MORE SUBSCRIBERS', 'MY WUBS GO HARDER', 'YOU DJ LIKE A TOASTER']},
    boss={'enter': ['Prepare for the drop!', 'I am the loudest thing alive!', 'Feel my bass!', 'Your ears will bleed!', 'The drop is here!'],
          'rev': ['Inverting your controls!', 'Left is right, noob!', 'Glitch mode!', 'Reversed frequencies!', 'Scrambled!'],
          'cor': ['Space bar compressed!', 'Your space is muted!', 'Sidechain this!', 'Space deleted!', 'Error: space not found!'],
          'fin': ['My woofers!', 'Too much bass!', 'Distortion critical!', 'Clipping!', 'Feedback loop!'],
          'ko': ['WUB... wub... wub...', 'Speaker blown!', 'Signal lost!', 'Silence!', 'Noooo bass!']},
    duet={'line': [''], 'atkLine': [''], 'atkWord': [''], 'healLine': [''], 'healReact': [''], 'healWord': ['']})

BUDDY_SAYS['cannon'] = ['FORTISSIMO!', 'FIRE THE OVERTURE!', 'FROM THE TOP!', 'CANNONS, TUTTI!', 'BRAVISSIMO!', 'MAESTRO, BOOM!']
CH[10] = dict(
    lines={'start': ['The curtain rises!', 'Allegro, let us begin!', 'From the top!', 'Bows ready!', 'A grand opening!'],
           'low': ['Stay in tempo!', 'Do not rush!', 'Mind the score!', 'Breathe, Vivi.', 'Find the melody!'],
           'recover': ['Back in harmony!', 'Bellissimo!', 'In tune again!', 'A tempo!', 'The music flows!'],
           'combo': ['Bravo!', 'Magnificent!', 'Virtuoso!', 'Crescendo!', 'Encore!'],
           'mini': ['Piano, silenced!', 'Lid closed!', 'Out of tune, out of time!', 'Grand finale!', 'Keys unlocked!'],
           'boss': ['The opera is saved!', 'Mortis, finale!', 'Curtain call!', 'Bravissima!', 'The music lives!'], 'fixed': ['']},
    rival={'start': ['My vibrato is better!', 'This stage is mine!', 'You call that a sonata?', 'Step aside, amateur!', 'Prepare to be outplayed!'],
           'win': ['Off tempo, darling!', 'Back to practice!', 'My encore!', 'Tone deaf!', 'Bravo, me!'],
           'kick': ['Bow strike!', 'Fortissimo kick!', 'Pizzicato poke!', 'Grace note slap!', 'Accent!'],
           'hurt': ['My bow!', 'My strings!', 'How uncouth!', 'My solo!', 'Not the Stradivarius!'],
           'taunts': ['YOUR BOW IS CROOKED', 'I PRACTICE 9 HOURS A DAY', 'NICE COAT. A RENTAL?', 'YOU PLAY LIKE A KAZOO', 'MY TEACHER WAS MOZART']},
    boss={'enter': ['Welcome to my requiem.', 'The organ demands silence!', 'Your final performance!', 'Bow before the maestro!', 'Play your last note.'],
          'rev': ['Play it in retrograde!', 'Backwards, little fiddler!', 'Your fingers are mine!', 'Inverted!', 'Dissonance!'],
          'broken': ['I will snap that bow!', 'No more violin!', 'Strings, be silent!', 'Your bow is mine!', 'Pizzicato no more!'],
          'fin': ['My organ pipes!', 'A wrong note!', 'Out of tune!', 'Not the crescendo!', 'The audience boos!'],
          'ko': ['My requiem!', 'Fine!', 'Curtain falls!', 'Coda!', 'Unfinished symphony!']},
    duet={'line': [''], 'atkLine': [''], 'atkWord': [''], 'healLine': [''], 'healReact': [''], 'healWord': ['']})

BUDDY_SAYS['cart'] = ['OI OI OI!', 'CART ATTACK!', 'NO RULES!', 'MOSH IN MOTION!', 'GET IN, LOSER!', 'PUNKS NOT DEAD!']
CH[11] = dict(
    lines={'start': ['Oi! Let us go!', 'One two three four!', 'Make some noise!', 'Riot time!', 'Turn it up to loud!'],
           'low': ['Do not give up!', 'Stay loud!', 'Never surrender!', 'Push back!', 'Keep fighting!'],
           'recover': ['Back in the pit!', 'Loud again!', 'That is punk!', 'Oi oi oi!', 'Still standing!'],
           'combo': ['Oi!', 'Loud and fast!', 'No rules!', 'Total chaos!', 'Mosh it!'],
           'mini': ['Mall cop down!', 'Shopping spree over!', 'Clean up on aisle you!', 'Security breached!', 'No more rules!'],
           'boss': ['Corporatron is bankrupt!', 'The street is ours!', 'Down with the suits!', 'Riot street is free!', 'Punks win!'], 'fixed': ['']},
    rival={'start': ['My mohawk is taller!', 'This street is mine!', 'Poser!', 'You call that punk?', 'Get lost, rookie!'],
           'win': ['Too slow, poser!', 'Sell out!', 'Back to the suburbs!', 'You are mainstream!', 'Ha! Loser!'],
           'kick': ['Boot!', 'Stage dive!', 'Mosh slam!', 'Headbutt!', 'Oi kick!'],
           'hurt': ['My mohawk!', 'My jacket!', 'Not cool!', 'My pins!', 'Ow, poser!'],
           'taunts': ['YOUR MOHAWK IS FLAT', 'I SAW THEM FIRST', 'NICE JACKET. FROM A MALL?', 'MY BAND HAS 3 FANS', 'YOU ARE SO MAINSTREAM']},
    boss={'enter': ['Your music is not profitable!', 'Sign here, punk!', 'Time to monetize you!', 'Welcome to the boardroom!', 'Rules are rules!'],
          'rev': ['Restructuring your controls!', 'Reversed, by policy!', 'Terms of service updated!', 'Synergy!', 'Rebranded!'],
          'cor': ['Your space is acquired!', 'Space: privatized!', 'Copyright strike!', 'Paywalled space!', 'Space bar, sold!'],
          'fin': ['My profits!', 'Stock is crashing!', 'Call my lawyers!', 'Not my bonus!', 'Hostile takeover!'],
          'ko': ['Bankrupt!', 'Market crash!', 'I am liquidated!', 'Fired!', 'Out of business!']},
    duet={'line': [''], 'atkLine': [''], 'atkWord': [''], 'healLine': [''], 'healReact': [''], 'healWord': ['']})

BUDDY_SAYS['pyro'] = ['FEUER FREI!', 'MORE FIRE!', 'IT IS GETTING HOT!', 'BURN IT DOWN!', 'FLAMES ON!', 'ACHTUNG, HOT!']
CH[12] = dict(
    lines={'start': ['Achtung! We begin!', 'Let the machines play!', 'Feel the steel!', 'Ja! Louder!', 'The harbor awakens!'],
           'low': ['Hold the rhythm!', 'Steel does not break!', 'Steady, steady!', 'March on!', 'Keep the machine running!'],
           'recover': ['Ja, much better!', 'Like clockwork!', 'The machine runs!', 'Precision!', 'Back in step!'],
           'combo': ['Wunderbar!', 'Ja! Ja! Ja!', 'Stahl!', 'Kraft!', 'Precision!'],
           'mini': ['Pressed flat!', 'The press is broken!', 'Out of order!', 'Under pressure? No.', 'Kaputt!'],
           'boss': ['The crane falls!', 'The harbor is free!', 'Kaputt, crane!', 'Steel wins!', 'Feierabend!'],
           'fixed': ['My guitar returns!', 'Ja, back in my hands!', 'Strings of steel!', 'Now we play again!', 'Wunderbar!']},
    rival={'start': ['My riff is heavier!', 'This harbor is mine!', 'You are too soft!', 'Achtung, amateur!', 'Prepare to be crushed!'],
           'win': ['Too slow!', 'Not precise enough!', 'Back to the factory!', 'I am the machine!', 'Kaputt!'],
           'kick': ['Stomp!', 'Steel toe!', 'Boot!', 'Heavy kick!', 'Hammer!'],
           'hurt': ['My goggles!', 'Rust!', 'Ow, sparks!', 'My boots!', 'Not the guitar!'],
           'taunts': ['YOUR BOOTS ARE CLEAN', 'MY PYRO IS BIGGER', 'YOU MARCH OFF BEAT', 'TOO MUCH FEELING', 'I EAT RIVETS']},
    boss={'enter': ['I am the iron crane!', 'All steel obeys me!', 'The harbor is mine!', 'Lift and crush!', 'Achtung, little worker!'],
          'rev': ['I turn your gears around!', 'Reverse the machine!', 'Wrong direction!', 'Backwards, worker!', 'Gears reversed!'],
          'broken': ['I lift your guitar!', 'Your guitar is cargo now!', 'Confiscated!', 'Hook and take!', 'No guitar for you!'],
          'fin': ['My cables!', 'Too much weight!', 'My hook!', 'Rust everywhere!', 'Structural failure!'],
          'ko': ['Kaputt...', 'Scrap metal!', 'I am rusting!', 'Collapse!', 'Out of service!']},
    duet={'line': [''], 'atkLine': [''], 'atkWord': [''], 'healLine': [''], 'healReact': [''], 'healWord': ['']})
