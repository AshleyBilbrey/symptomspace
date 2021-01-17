(function()
{
    const quotes = [        
`“The human capacity for burden is like bamboo – far more flexible than you’d ever believe at first glance.” — Jodi Picoult`,
`“I can be changed by what happens to me. But I refuse to be reduced by it.” — Maya Angelou`,
`“On the other side of a storm is the strength that comes from having navigated through it. Raise your sail and begin.” — Gregory S. Williams`,
`“Although the world is full of suffering, it is also full of the overcoming of it.” — Helen Keller`,
`“Turn your wounds into wisdom.” — Oprah Winfrey`,
`“My scars remind me that I did indeed survive my deepest wounds. That in itself is an accomplishment. And they bring to mind something else, too. They remind me that the damage life has inflicted on me has, in many places, left me stronger and more resilient. What hurt me in the past has actually made me better equipped to face the present.” — Steve Goodier`,
`“Resilience is accepting your new reality, even if it’s less good than the one you had before. You can fight it, you can do nothing but scream about what you’ve lost, or you can accept that and try to put together something that’s good.” — Elizabeth Edwards`,
`“A good half of the art of living is resilience.” — Alain de Botton`,
`“Never say that you can’t do something, or that something seems impossible, or that something can’t be done, no matter how discouraging or harrowing it may be; human beings are limited only by what we allow ourselves to be limited by: our own minds. We are each the masters of our own reality; when we become self-aware to this: absolutely anything in the world is possible.” — Mike Norton`,
`“Life doesn’t get easier or more forgiving, we get stronger and more resilient.” — Steve Maraboli`,
`“We all have battles to fight. And it’s often in those battles that we are most alive: it’s on the frontlines of our lives that we earn wisdom, create joy, forge friendships, discover happiness, find love, and do purposeful work.” — Eric Greitens`,
`“No matter how much falls on us, we keep plowing ahead. That’s the only way to keep the roads clear.” — Greg Kincaid`,
`“Resilience is very different than being numb. Resilience means you experience, you feel, you fail, you hurt. You fall. But, you keep going.” — Yasmin Mogahed`,
`“The oak fought the wind and was broken, the willow bent when it must and survived.” — Robert Jordan`,
`“You must bear losses like a soldier, the voice told me, bravely and without complaint, and just when the day seems lost, grab your shield for another stand, another thrust forward. That is the juncture that separates heroes from the merely strong.” — Margaret George`,
`“Strong people alone know how to organize their suffering so as to bear only the most necessary pain.” — Emil Dorian`,
`“Some knowledge is too heavy…you cannot bear it…your Father will carry it until you are able.” — Corrie ten Boom`,
`“Strength does not come from winning. Your struggles develop your strengths. When you go through hardships and decide not to surrender, that is strength.” — Arnold Schwarzenegger`,
`“No one escapes pain, fear, and suffering. Yet from pain can come wisdom, from fear can come courage, from suffering can come strength – if we have the virtue of resilience.” — Eric Greitens`,
`“I believe in being strong when everything seems to be going wrong… I believe that tomorrow is another day and I believe in miracles.” — Audrey Hepburn`,
`“The difference between a strong man and a weak one is that the former does not give up after a defeat.” — Woodrow Wilson`,
`“Hold yourself responsible for a higher standard than anybody else expects of you. Never excuse yourself. Never pity yourself. Be a hard master to yourself-and be lenient to everybody else.” — Henry Ward Beecher`,
`“I hope you never fear those mountains in the distance,`,
`Never settle for the path of least resistance.” — Lee Ann Womack`,
`“Life is very interesting. In the end, some of your greatest pains become your greatest strengths.” — Drew Barrymore`,
`“My barn having burned down, I can now see the moon.” — Mizuta Masahide`,
`“If you’re going through hell, keep going.” — Winston Churchill`,
`“Enthusiasm is common. Endurance is rare.” — Angela Duckworth`,
`“Listen to the people who love you. Believe that they are worth living for even when you don’t believe it. Seek out the memories depression takes away and project them into the future. Be brave; be strong; take your pills. Exercise because it’s good for you even if every step weighs a thousand pounds. Eat when food itself disgusts you. Reason with yourself when you have lost your reason.” — Andrew Solomon`,
`“We are all faced with a series of great opportunities brilliantly disguised as impossible situations.” — Chuck Swindoll`,
`“Resilience is the ability to attack while running away.” — Wes Fessler`,
`“You may have to fight a battle more than once to win it.” — Margaret Thatcher`,
`“Rock bottom became the solid foundation in which I rebuilt my life.” — J.K. Rowling`,
`“That which does not kill us makes us stronger.” — Friedrich Nietzsche`,
`“One’s dignity may be assaulted, vandalized and cruelly mocked, but it can never be taken away unless it is surrendered.” — Michael J. Fox`,
`“The harder you fall, the heavier your heart; the heavier your heart, the stronger you climb; the stronger you climb, the higher your pedestal.” — Criss Jami`,
`“Successful people demonstrate their resilience through their dedication to making progress every day, even if that progress is marginal.” — Jonathan Mills`,
`“You have power over your mind – not outside events. Realize this, and you will find strength.” — Marcus Aurelius`,
`“Failure will never overtake me if my determination to succeed is strong enough.” — Og Mandino`,
`“With the new day comes new strength and new thoughts.” — Eleanor Roosevelt`,
`“Resilience isn’t a single skill. It’s a variety of skills and coping mechanisms. To bounce back from bumps in the road as well as failures, you should focus on emphasizing the positive.” — Jean Chatzky`,
`“I love the man that can smile in trouble, that can gather strength from distress, and grow brave by reflection. ’Tis the business of little minds to shrink, but he whose heart is firm, and whose conscience approves his conduct, will pursue his principles unto death.” — Thomas Paine`,
`“Hard times don’t create heroes. It is during the hard times when the ‘hero’ within us is revealed.” — Bob Riley`,
`“What helps you persevere is your resilience and commitment.” — Roy T. Bennett`,
`“It’s a funny thing about life, once you begin to take note of the things you are grateful for, you begin to lose sight of the things that you lack.” — Germany Kent`,
`“If your heart is broken, make art with the pieces.” — Shane Koyczan`,
`“Nothing is more beautiful than the smile that has struggled through the tears.” — Demi Lovato`,
`“Out of suffering have emerged the strongest souls; the most massive characters are seared with scars.” — Khalil Gibran`,
`“Hard times may have held you down, but they will not last forever. When all is said and done, you will be increased.” — Joel Osteen`,
`“The world breaks everyone, and afterward, some are strong at the broken places.” — Ernest Hemingway`,
`“It is really wonderful how much resilience there is in human nature. Let any obstructing cause, no matter what, be removed in any way, even by death, and we fly back to first principles of hope and enjoyment.” — Bram Stoker`,
`“Hard times are sometimes blessings in disguise. We do have to suffer but in the end it makes us strong, better and wise.” — Anurag Prakash Ray`,
`“Persistence and resilience only come from having been given the chance to work through difficult problems.” — Gever Tulley`,
`“Difficulties are meant to rouse, not discourage. The human spirit is to grow strong by conflict.” — William Ellery Channing`,
`“I have no regrets in my life. I think that everything happens to you for a reason. The hard times that you go through build character, making you a much stronger person.” — Rita Mero`,
`“Do not judge me by my success, judge me by how many times I fell down and got back up again.” — Nelson Mandela`,
`“Hard times arouse an instinctive desire for authenticity.” — Coco Chanel`,
`“There is a saying in Tibetan, ‘Tragedy should be utilized as a source of strength.’ No matter what sort of difficulties, how painful experience is, if we lose our hope, that’s our real disaster.” — 14th Dalai Lama`,
`“We are only as strong as we are united, as weak as we are divided.” — J.K. Rowling`,
`“No matter how bleak or menacing a situation may appear, it does not entirely own us. It can’t take away our freedom to respond, our power to take action.” — Ryder Carroll`,
`“You never know how strong you are, until being strong is your only choice.” — Bob Marley`,
`“Anyone can give up; it is the easiest thing in the world to do. But to hold it together when everyone would expect you to fall apart, now that is true strength.” — Chris Bradford`,
`“Like tiny seeds with potent power to push through tough ground and become mighty trees, we hold innate reserves of unimaginable strength. We are resilient.” — Catherine DeVrye`,
`“Our greatest weakness lies in giving up. The most certain way to succeed is always to try just one more time.” — Thomas Edison`,
`“She stood in the storm and when the wind did not blow her way, she adjusted her sails.” — Elizabeth Edwards`,
`“Courage is the most important of all the virtues because without courage, you can’t practice any other virtue consistently.” — Maya Angelou`,
`“All the adversity I’ve had in my life, all my troubles and obstacles, have strengthened me…. You may not realize it when it happens, but a kick in the teeth may be the best thing in the world for you.” — Walt Disney`,
`“He who believes is strong; he who doubts is weak. Strong convictions precede great actions.” — Louisa May Alcott`,
`“Our greatest glory is not in never falling, but in rising every time we fall.” — Confucius`,
`“Hard times build determination and inner strength. Through them we can also come to appreciate the uselessness of anger.” — Dalai Lama`,
`“Be patient and tough; someday this pain will be useful to you.” — Ovid`,
`“Only those who dare to fail greatly, can ever achieve greatly.” — Robert F. Kennedy`,
`“Make up your mind that no matter what comes your way, no matter how difficult, no matter how unfair, you will do more than simply survive. You will thrive in spite of it.” — Joel Osteen`,
`“Grief and resilience live together.” — Michelle Obama`,
`“We are not a product of what has happened to us in our past. We have the power of choice.” — Stephen Covey`,
`“When we learn how to become resilient, we learn how to embrace the beautifully broad spectrum of the human experience.” — Jaeda Dewalt`,
`“We do not have to become heroes overnight. Just a step at a time, meeting each thing that comes up, seeing it is not as dreadful as it appeared, discovering we have the strength to stare it down.” — Eleanor Roosevelt`,
`“Resilience is based on compassion for ourselves as well as compassion for others.” — Sharon Salzberg`,
`“Worry does not empty tomorrow of its sorrow. It empties today of its strength.” — Corrie ten Boom`,
`“Every adversity, every failure, and every heartache, carries with it the seed of an equivalent or greater benefit.” — Napoleon Hill`,
`“Confidence, courage and determined spirit are vital for surviving hard times.” — Lailah Gifty Akita`,
`“Hope is the thing with feathers that perches in the soul – and sings the tunes without the words – and never stops at all.” — Emily Dickinson`,
`“When things are bad, we take comfort in the thought that they could always get worse. And when they are, we find hope in the thought that things are so bad they have to get better.” — Malcolm S. Forbes`,
`“We must accept finite disappointment, but never lose infinite hope.” — Martin Luther King, Jr.`,
`“The gem cannot be polished without friction, nor man perfected without trials.” — Chinese Proverb`,
`“Worry never robs tomorrow of its sorrow, it only saps today of its joy.” — Leo Buscaglia`,
`“And hard times are good in their own way, too. Because the only way you can achieve true happiness is if you experience true sadness as well. It’s all about light and shade. Balance.” — Gabrielle Williams`,
`“In the middle of difficulty lies opportunity.” — Albert Einstein`,
`“When everything seems to be going against you, remember that the airplane takes off against the wind, not with it.” — Henry Ford`,
`“Going through challenging things can teach you a lot, and they also make you appreciate the times that aren’t so challenging.” — Carrie Fisher`,
`“You may not always have a comfortable life and you will not always be able to solve all of the world’s problems at once but don’t ever underestimate the importance you can have because history has shown us that courage can be contagious and hope can take on a life of its own.” — Michelle Obama`,
]
    document.querySelector('#inspo').textContent = quotes[Math.floor(Math.random() * quotes.length)];
})()