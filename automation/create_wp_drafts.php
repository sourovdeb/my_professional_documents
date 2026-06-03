<?php
/**
 * WordPress Draft Creator — Sourov Deb
 * Upload this file to WordPress via deploy.php, then call it once.
 * It creates all 6 blog posts as DRAFTS (status=draft) in WordPress.
 * Delete this file after running it.
 *
 * Upload path: /home/u839078121/domains/sourovdeb.com/public_html/wp-content/
 * Run URL: https://www.sourovdeb.com/wp-content/create_wp_drafts.php?key=0767044896thevenet_
 */

// Simple key check
if (!isset($_GET['key']) || $_GET['key'] !== '0767044896thevenet_') {
    http_response_code(403);
    die('Forbidden');
}

// Bootstrap WordPress
$wp_load = dirname(__DIR__) . '/wp-load.php';
if (!file_exists($wp_load)) {
    die('wp-load.php not found at: ' . $wp_load);
}
require_once $wp_load;

if (!function_exists('wp_insert_post')) {
    die('WordPress not loaded correctly.');
}

$posts = [
    [
        'title'    => 'The Ship With a Broken Compass',
        'slug'     => 'ship-with-broken-compass',
        'category' => 'Mental Health',
        'tags'     => ['bipolar', 'ADHD', 'PTSD', 'resilience', 'neurodiversity', 'lived experience'],
        'excerpt'  => 'A personal essay about navigating life with bipolar disorder, ADHD and complex trauma — and finding that the broken compass was never the real problem.',
        'content'  => <<<HTML
<p>I sailed for twenty years without knowing my compass was broken.</p>

<p>Not metaphorically. Literally: I built a career in luxury hospitality across Sydney's finest venues. I learned four languages. I managed multilingual teams. I charmed clients in three currencies. And the whole time, my brain was navigating with faulty instruments — pulling me left when I meant to go right, surging forward at 3am when I needed sleep, stalling completely when all I needed to do was send one email.</p>

<p>I know now. Back then, I just thought I was difficult.</p>

<p>Here is what a broken compass looks like from the inside: you are brilliant at emergencies and terrible at Tuesdays. A restaurant floor in crisis? You are the calmest person in the room. A long-term project with no deadline? You spend four hours rearranging the desktop icons and call it work. You speak four languages and still cannot finish a sentence to the person who loves you most. You survive things that would flatten other people — and then fall apart over a parking ticket.</p>

<p>I grew up in Chittagong, Bangladesh, the oldest child of two people who could not stop fighting. My job, from the time I was about thirteen, was to keep the house from splitting apart. I became very good at reading rooms — feeling the tension before it cracked, knowing what each person needed before they asked, absorbing what nobody else wanted to carry. That skill made me exceptional at hospitality. It also meant I had been doing other people's emotional labour since before I had a word for it.</p>

<p>I moved to Australia in 2005 thinking distance would fix things. It did not. My parents called separately, each one asking me to take their side, one or two hours per call. I was twenty years old and I was already exhausted. I spent two years making bad choices — not to be reckless, but to stop feeling like I was responsible for everything and everyone at once. Nobody explained to me that this is what an undiagnosed, untreated, traumatised brain does when it runs out of options. I just thought I was weak.</p>

<p>I was not weak. I was unequipped.</p>

<p>The diagnosis came in La Réunion, where I now live with my wife — the best decision of my life — and our daughter. A GP told me I was depressed "like big time." A psychiatrist eventually named the fuller picture. Four decades of my life clicked into place in one afternoon.</p>

<p>This is not a story about despair. It is a story about what happens when you finally get accurate instruments.</p>

<p>A broken compass does not make you a bad sailor. It just means every destination took longer than it should have, every storm was harder than it needed to be, and the miracle is not that you arrived — it is that you kept going without knowing where you were.</p>

<p>I kept going. I am still going. And now I know where I am.</p>

<p>If you are reading this and your compass feels broken too: welcome. You are in good company. And the sea is not as large as it looks.</p>

<hr>
<p><em>Sourov Deb is a multilingual writer, educator and advocate living in La Réunion. He writes about mental health, neurodiversity, language and the unglamorous business of rebuilding a life.</em></p>
HTML,
    ],
    [
        'title'    => 'What Bipolar Taught Me That Every Productivity Guru Got Wrong',
        'slug'     => 'bipolar-productivity-truth',
        'category' => 'Productivity',
        'tags'     => ['bipolar', 'productivity', 'ADHD', 'neurodivergent', 'stability', 'routine'],
        'excerpt'  => 'Every productivity system I tried made me worse. Here is what finally worked — and why it starts with a rule that sounds like giving up.',
        'content'  => <<<HTML
<p>Every productivity system I ever tried made me worse.</p>

<p>Not slightly worse. Significantly, measurably, sometimes dangerously worse. I tried time-blocking. I tried the Pomodoro Technique. I tried morning pages and bullet journals and eating the frog. Each one worked for about eleven days — roughly the length of my attention span when something is new and stimulating — and then collapsed in exactly the way the person selling the system promised it would not.</p>

<p>For years I blamed myself. Then I got a diagnosis that explained everything, and I realised I had been trying to put diesel in a petrol engine and wondering why it sputtered.</p>

<p>Here is what nobody in the productivity industry tells you about bipolar disorder: the energy you feel during a hypomanic or manic phase feels exactly like motivation. It feels like finally getting it together. It feels like the version of yourself you have always wanted to be. And so you ride it. You work until 2am. You start three projects. You send the email you have been avoiding for six weeks. You feel invincible.</p>

<p>And then you crash. Every time.</p>

<p>The crash does not feel like failure of character. It feels like falling off a cliff you did not know was there. And because you rode the energy up instead of protecting it, the cliff is higher, the fall is longer, and the recovery takes weeks you do not have.</p>

<p>I learned this the hard way. My psychiatrist explained the mechanism, and I built a new system around one principle that sounds like giving up but is actually the most ambitious thing I have ever done:</p>

<p><strong>Protect the rhythm before the output.</strong></p>

<p>Fixed wake time. Fixed meals. Fixed wind-down. Not because I am lazy. Because my nervous system is a precision instrument that needs calibration more than it needs acceleration. I am not trying to produce less. I am trying to produce consistently — which, for a brain like mine, requires treating my sleep and my schedule like infrastructure rather than obstacles.</p>

<p>The productivity gurus sell the idea that you need to maximise your best days. The truth — for those of us with bipolar disorder — is that we need to survive our worst ones without making the next cycle harder.</p>

<p>Stability is not the enemy of output. It is the only thing that makes consistent output possible.</p>

<p>That is not giving up. That is finally working with yourself instead of against yourself.</p>

<hr>
<p><em>Sourov Deb lives in La Réunion. He writes about mental health, neurodiversity, and what actually works when the standard advice fails.</em></p>
HTML,
    ],
    [
        'title'    => 'The Forensic Auditor: How Documentation Became My Therapy',
        'slug'     => 'forensic-auditor-documentation-healing',
        'category' => 'Advocacy',
        'tags'     => ['advocacy', 'gaslighting', 'CELTA', 'neurodiversity', 'documentation', 'disability rights', 'PTSD'],
        'excerpt'  => 'When an institution rewrote my reality, I stopped fighting for an apology and started building a record.',
        'content'  => <<<HTML
<p>At some point during my dispute with a language teacher training institution, I stopped trying to win and started trying to document.</p>

<p>This is not the same thing. And understanding the difference changed everything.</p>

<p>I had completed my teaching hours. I had passed my written assignments. I had received a "to standard" verdict on my final teaching practice. Then, within 72 hours, the assessment shifted. An official document was retroactively amended. When I pointed to the contradiction, I was told it was a typo.</p>

<p>This is what gaslighting looks like in an institutional setting: slow, polite, perfectly deniable.</p>

<p>For a man who grew up in a home where the adults in the room regularly rewrote reality — where being told you remembered it wrong was a survival strategy used against you before you could read — this was not just a bureaucratic dispute. This was the childhood nightmare in a suit and tie.</p>

<p>My first instinct was the instinct of every traumatised person: go silent and absorb it. My second instinct — the one that arrived a few days later, quieter but steadier — was different. It said: you have something you never had as a child. You have receipts.</p>

<p>I named the role myself: Forensic Auditor. Not plaintiff. Not victim. Auditor — the person who reads the numbers and lets the numbers speak.</p>

<p>What I did next was methodical. I printed every email. I timestamped every communication. I cross-referenced published assessment criteria against what I was told in the room. I filed a formal complaint with procedural errors documented. I sent a complaint to the national education regulator. I built a case not to win an apology — I knew I would not get one — but to create an undeniable public record that my reality happened and cannot be erased.</p>

<p>Documentation is not aggression. It is memory made material. For those of us who grew up being told we remembered it wrong, a timestamped email is something profound: proof that you are not inventing it.</p>

<p>The goal does not have to be victory. My real goal was to be the first version of myself who, when told his experience did not happen, could point to a folder and say: it is all in here.</p>

<p>For a brain that spent forty years believing that speaking up only created more problems, building a paper trail was the most radical act of self-respect I have ever performed.</p>

<p>I am still in the middle of this. Regulators are reviewing. No verdict has been reached. But that is not the point.</p>

<p>The point is that this time, I did not go silent. That is not litigation. That is healing.</p>

<hr>
<p><em>Sourov Deb is currently pursuing a formal regulatory complaint against a Cambridge-accredited language training centre. He writes about education, disability rights and the intersection of trauma and advocacy.</em></p>
HTML,
    ],
    [
        'title'    => 'Five Languages, One Voice: Why I Never Felt Smart Enough',
        'slug'     => 'five-languages-one-voice-multilingualism-adhd',
        'category' => 'Language',
        'tags'     => ['multilingualism', 'imposter syndrome', 'language learning', 'ADHD', 'identity', 'neurodivergent'],
        'excerpt'  => 'I speak five languages and spent most of my life convinced I was not intelligent. This is what multilingualism and ADHD look like from the inside.',
        'content'  => <<<HTML
<p>I speak five languages. Bengali is the first one — the one I dreamed in as a child, the one I still argue in when I lose my temper. English is the one I built a career in across eleven years of Sydney's luxury hospitality circuit. French is the one my daughter will grow up in, on this island in the Indian Ocean. Arabic and some Japanese arrived somewhere in between, at bars and airports and kitchens, absorbed the way languages come to people who have always been listening more than talking.</p>

<p>For most of my life, I did not consider this a sign of intelligence.</p>

<p>I considered it noise. Evidence of distraction. Proof that I could not commit to anything long enough to do it properly.</p>

<p>This is what undiagnosed ADHD does to your self-story. It turns your strengths into accusations. You are multilingual? That is because you cannot sit still in one country. You switch between tasks effortlessly? That is because you cannot finish anything.</p>

<p>I was reading books in English when other kids in Chittagong were still sounding out letters. By the time I arrived in Australia at nineteen, I was already fluent. By the time I moved to France's overseas territory, I had added French to the stack. Languages, for a brain like mine, are not academic exercises. They are survival tools, social camouflage, portals into entirely different modes of being. In French I am more formal, more deliberate. In English I am dry and fast. In Bengali I am the child who never quite grew up.</p>

<p>No school ever told me this was remarkable. What school told me — repeatedly, in three countries — was that I could not concentrate and I did not finish things.</p>

<p>Both were true. Neither was the full picture.</p>

<p>Here is what I know now that I did not know then: multilingualism and ADHD often share a brain. The same hyperfocus that makes sustained attention in a quiet classroom impossible makes total immersion in a new language irresistible. The same restlessness that burned through semesters makes a packed service floor feel like a natural habitat.</p>

<p>I am not smart despite my ADHD. I am multilingual because of it.</p>

<p>That is not a consolation prize. That is the actual prize.</p>

<p>I just had to learn to name it correctly.</p>

<hr>
<p><em>Sourov Deb is a multilingual educator and writer based in La Réunion. He teaches English and writes about language, identity and neurodiversity.</em></p>
HTML,
    ],
    [
        'title'    => 'Generational Trauma Stops Here',
        'slug'     => 'generational-trauma-stops-here',
        'category' => 'Mental Health',
        'tags'     => ['generational trauma', 'parenting', 'bipolar', 'healing', 'PTSD', 'Bangladesh', 'diaspora', 'fatherhood'],
        'excerpt'  => 'My parents did not choose to hurt me. They were hurt first. I choose to be the last link in this chain.',
        'content'  => <<<HTML
<p>My parents loved me. I believe that completely.</p>

<p>They also hurt me. I believe that completely too.</p>

<p>These two things are not contradictions. They are the definition of generational trauma: pain that moves from one body to the next, not because the people carrying it are cruel, but because they never had the language or the tools to put it down. My mother was beaten as a child. My father grew up performing for a grandfather who measured love in achievements and money. Neither of them ever sat with a therapist. Neither of them ever heard the words "that was not your fault." So they did to me what had been done to them, imperfectly and with love, and I spent four decades unpacking it.</p>

<p>I have a daughter now. She is eighteen months old. She is, without question, the most important thing in my life — the reason everything else I am doing has to succeed, and the reason I cannot afford to pretend I have not inherited something I need to put down.</p>

<p>Here is what I mean by breaking the cycle, in concrete terms, because I am tired of reading abstract things about generational trauma that do not tell you what to actually do:</p>

<p><strong>I name my emotions out loud.</strong> When I am anxious, I say "I am anxious right now." Not to burden her — she is a baby, she does not understand — but to rewire myself, because I grew up in a house where emotion had no name and no space.</p>

<p><strong>I apologise when I am wrong.</strong> No adult in my childhood ever said sorry to me — not for the big things, not for the small ones. An apology requires you to believe the other person's experience is real.</p>

<p><strong>I protect my own health like it is her future.</strong> Because it is. My stability is her emotional baseline. When I manage my condition well, she gets the version of me who can be present.</p>

<p><strong>I am in therapy.</strong> I say this without shame. My father would have said it was weakness. I say: the conversation I am having now is the one they never had, and it stops here.</p>

<p>None of this is finished. I am still in it. But my daughter will grow up knowing that her father looked at the thing he inherited, called it by its real name, and chose to stop.</p>

<p>That is the only legacy worth building.</p>

<hr>
<p><em>Sourov Deb is a writer and educator in La Réunion. He is a father, a trauma survivor, and a work in progress.</em></p>
HTML,
    ],
    [
        'title'    => 'The Neurodivergent Writer\'s Toolkit: What Actually Works (2026)',
        'slug'     => 'neurodivergent-writers-toolkit-2026',
        'category' => 'Tools',
        'tags'     => ['ADHD', 'bipolar', 'tools', 'writing', 'productivity', 'free tools', 'open source', 'neurodivergent'],
        'excerpt'  => 'Not a sponsored roundup. These are the tools that a multilingual writer with ADHD and bipolar disorder actually uses.',
        'content'  => <<<HTML
<p>I am going to save you some time. Most "productivity tool" roundups are written by people with executive function who are trying to optimize. This one is written by someone with ADHD and bipolar disorder who is trying to survive.</p>

<p>Different problem. Different tools.</p>

<h2>For Writing</h2>

<p><strong>Obsidian</strong> (free) — All my drafts live here. Local files, no subscription, works offline. For a brain that forgets what it was doing the moment the internet goes down, local storage is not a preference, it is a requirement.</p>

<p><strong>LanguageTool</strong> (free tier) — Better than Grammarly for multilingual writers. I switch between English and French in the same document and it does not panic.</p>

<p><strong>Hemingway Editor</strong> (free, browser) — Paste your draft in and it highlights every passive sentence, every adverb, every thing you do to hide that you are not sure what you are saying. Brutal. Useful.</p>

<h2>For Focus</h2>

<p><strong>Forest</strong> (free tier) — You plant a tree. The tree dies if you pick up your phone. This sounds childish and it works completely. For a dopamine-seeking brain, the visual cost of breaking focus is more effective than any reminder.</p>

<p><strong>Goblin Tools</strong> (free) — Break any task into micro-steps. Type "write blog post," ask it to break this down into seven steps, suddenly I can start.</p>

<h2>For Scheduling and Stability</h2>

<p><strong>Tiimo</strong> (free tier) — Visual daily planner designed for neurodivergent users. Not a to-do list. A schedule with colour and duration, so I can see my day rather than read it.</p>

<p><strong>Leantime</strong> (open source) — Project management that accounts for how neurodivergent brains work. Self-hostable, no subscription, no data selling.</p>

<h2>For Automation</h2>

<p><strong>n8n</strong> (open source, self-hostable) — Connect your apps with visual workflows. I use it to move draft files from one place to another automatically. The learning curve is real but the payoff is permanent.</p>

<p><strong>Otter.ai</strong> (free tier) — Speak your first draft. I am a much better talker than typist when I am dysregulated. Otter transcribes and timestamps. Five hundred words in twenty minutes instead of two hours.</p>

<h2>The Honest Rule</h2>

<p>No tool will substitute for the fundamental work of understanding your own cycles and protecting your sleep. But the right tools reduce the friction between having an idea and getting it out of your head.</p>

<p>That friction is the enemy. Every tool here attacks it.</p>

<hr>
<p><em>Sourov Deb writes about neurodiversity, language and survival. He does not accept sponsored content.</em></p>
HTML,
    ],
];

$results = [];
$author_id = 1; // Default admin user ID

foreach ($posts as $post) {
    // Get or create category
    $category_id = 0;
    $term = get_term_by('name', $post['category'], 'category');
    if ($term) {
        $category_id = $term->term_id;
    } else {
        $new_term = wp_insert_term($post['category'], 'category');
        $category_id = is_wp_error($new_term) ? 0 : $new_term['term_id'];
    }

    // Create post
    $post_data = [
        'post_title'   => wp_strip_all_tags($post['title']),
        'post_content' => $post['content'],
        'post_excerpt' => $post['excerpt'],
        'post_status'  => 'draft',
        'post_author'  => $author_id,
        'post_name'    => $post['slug'],
        'post_category' => [$category_id],
    ];

    $post_id = wp_insert_post($post_data, true);

    if (is_wp_error($post_id)) {
        $results[] = ['title' => $post['title'], 'status' => 'error', 'message' => $post_id->get_error_message()];
        continue;
    }

    // Set tags
    wp_set_post_tags($post_id, $post['tags'], false);

    // Set Yoast SEO meta if available
    update_post_meta($post_id, '_yoast_wpseo_metadesc', $post['excerpt']);

    $results[] = [
        'title'   => $post['title'],
        'post_id' => $post_id,
        'status'  => 'created',
        'edit_url' => admin_url("post.php?post={$post_id}&action=edit"),
    ];
}

// Output results
header('Content-Type: application/json');
echo json_encode(['success' => true, 'posts_created' => count($results), 'results' => $results], JSON_PRETTY_PRINT);

// Self-delete after successful run (optional — comment out if you want to keep it)
// unlink(__FILE__);
