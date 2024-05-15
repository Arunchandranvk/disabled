document.addEventListener('DOMContentLoaded', function () {
    const alphabetSounds = {
        'A': '{% static "sounds/a.mp3" %}',
        'B': "{% static  'sounds/b.mp3'  %}",
        'C': "{% static  'sounds/c.mp3' %}",
        'D': "{% static  'sounds/d.mp3' %}",
        'E': "{% static  'sounds/e.mp3' %}",
        'F': "{% static  'sounds/f.mp3' %}",
        'G': "{% static  'sounds/g.mp3' %}",
        'H': "{% static  'sounds/h.mp3' %}",
        'I': "{% static  'sounds/i.mp3' %}",
        'J': "{% static  'sounds/j.mp3' %}",
        'K': "{% static  'sounds/k.mp3' %}",
        'L': "{% static  'sounds/l.mp3' %}",
        'M': "{% static  'sounds/m.mp3' %}",
        'N': "{% static  'sounds/n.mp3' %}",
        'O': "{% static  'sounds/o.mp3' %}",
        'P': "{% static  'sounds/p.mp3' %}",
        'Q': "{% static  'sounds/q.mp3' %}",
        'R': "{% static  'sounds/r.mp3' %}",
        'S': "{% static  'sounds/s.mp3' %}",
        'T': "{% static  'sounds/t.mp3' %}",
        'U': "{% static  'sounds/u.mp3' %}",
        'V': "{% static  'sounds/v.mp3' %}",
        'W': "{% static  'sounds/w.mp3' %}",
        'X': "{% static  'sounds/x.mp3' %}",
        'Y': "{% static  'sounds/y.mp3' %}",
        'Z': "{% static  'sounds/z.mp3' %}",
    };

    const playButton = document.getElementById('playButton');
    const letterContainer = document.getElementById('letter-container');
    const scoreElement = document.getElementById('score-value');
    const resultElement = document.getElementById('result');
    let score = 0;
    let rounds = 0;

    playButton.addEventListener('click', playRandomAlphabet);

    function playSound(letter) {
        const audio = new Audio(alphabetSounds[letter]);
        audio.play();
    }

    function playRandomAlphabet() {
        if (rounds < 10) {
            rounds++;
            const alphabetKeys = Object.keys(alphabetSounds);
            const randomAlphabet = alphabetKeys[Math.floor(Math.random() * alphabetKeys.length)];
            playSound(randomAlphabet);
            letterContainer.textContent = ''; 
            setTimeout(() => {
                letterContainer.textContent = randomAlphabet;
            }, 1500);

        } else {
            displayFinalScore();
        }
    }

    function displayFinalScore() {
        resultElement.textContent = `Game Over! Your final score is ${score}.`;
        playButton.disabled = true;
    }

    document.addEventListener('keydown', function (event) {
        const keyPressed = event.key.toUpperCase();
        if (Object.keys(alphabetSounds).includes(keyPressed)) {
            if (keyPressed === letterContainer.textContent) {
                score++;
                scoreElement.textContent = score;
            }
            
            playRandomAlphabet();
        }
    });
});
