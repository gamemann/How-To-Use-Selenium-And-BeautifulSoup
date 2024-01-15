import { useState } from 'react';
import './App.css';

// Images
const images = [
  "/images/testimage01.png",
  "/images/testimage02.png",
  "/images/testimage03.png",
  "/images/testimage04.png"
]

// Cards
type Card = {
  title: string
  description: JSX.Element
}

const cards: Card[] = [
  {
    title: "Card Title #1",
    description: <span>This is the description of <span style={{ fontWeight: "bold" }}>card #1</span>!</span>
  },
  {
    title: "Card Title #2",
    description: <span>This is the description of <span style={{ fontWeight: "bold" }}>card #2</span>!</span>
  },
  {
    title: "Card Title #3",
    description: <span>This is the description of <span style={{ fontWeight: "bold" }}>card #3</span>!</span>
  }
]

// Clickable Dividers.
type ClickDiv = {
  title: string
  contents: JSX.Element
}

const clickDivs: ClickDiv[] = [
  {
    title: "Clickable Div #1",
    contents: <span>These are the hidden contents of <span style={{ fontWeight: "bold" }}>clickable div #1</span>!</span>
  },
  {
    title: "Clickable Div #2",
    contents: <span>These are the hidden contents of <span style={{ fontWeight: "bold" }}>clickable div #2</span>!</span>
  },
  {
    title: "Clickable Div #3",
    contents: <span>These are the hidden contents of <span style={{ fontWeight: "bold" }}>clickable div #3</span>!</span>
  },
  {
    title: "Clickable Div #4",
    contents: <span>These are the hidden contents of <span style={{ fontWeight: "bold" }}>clickable div #4</span>!</span>
  }
]

function App() {
  return (
    <div className="App">
      <div id="images">
        <h1>Images</h1>
        <div>
          {images.map((img, index) => {
            return (
              <Image
                key={`image-${index.toString()}`}
                url={img}
                index={index}
              />
            )
          })}
        </div>
      </div>
      <div id="cards">
        <h1>Cards</h1>
        <div>
          {cards.map((card, index) => {
            return (
              <Card
                key={`index-${index.toString()}`}
                card={card}
              />
            )
          })}
        </div>
      </div>
      <div id="clickDivs">
        <h1>Clickable Divs</h1>
        <div>
          {clickDivs.map((clickDiv, index) => {
            return (
              <ClickDiv
                key={`clickDiv-${index.toString()}`}
                clickDiv={clickDiv}
              />
            )
          })}
        </div>
      </div>
    </div>
  );
}

function Image ({
  url,
  index
} : {
  url: string
  index: number
}) {
  return (
    <div className="image-row">
      <img
        src={url}
        alt={`Alt #${(index + 1).toString()}`}
      />
    </div>
  )
}

function Card ({
  card
} : {
  card: Card
}) {
  return (
    <div className="card-row">
      <h2>{card.title}</h2>
      <p>{card.description}</p>
    </div>
  )
}

function ClickDiv ({
  clickDiv
} : {
  clickDiv: ClickDiv
}) {
  // Controls state of showing/hiding contents.
  const [visible, setVisible] = useState(false);

  return (
    <div
      className="clickDiv-row"
      onClick={() => setVisible(!visible)}
    >
      <h2>{clickDiv.title}</h2>
      {visible && (
        <div>
          {clickDiv.contents}
        </div>
      )}
    </div>
  )
}

export default App;
