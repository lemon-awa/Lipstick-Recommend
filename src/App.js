import { useEffect, useState } from "react";
import "./style.css";
import { initialFacts } from "./data";
import { COLOR_CATEGORIES } from "./color";

// const COLOR_CATEGORIES = [
//   { name: "red", color: "#ef4444" },
//   { name: "pink", color: "#db2777" },
//   { name: "orange", color: "#f97316" },
// ];

const BENEFIT_CATEGORIES = [
  { name: "Hydrating", color: "#3b82f6" },
  { name: "Long-wearing", color: "#16a34a" },
  { name: "Plumping", color: "#ef4444" },
  { name: "Transfer-resistant", color: "#eab308" },
  { name: "Transfer-proof", color: "#db2777" },
  { name: "Waterproof", color: "#14b8a6" },
];

const PRICE_CATEGORIES = [
  { name: "Under $25", color: "#8f8989" },
  { name: "$25 to $50", color: "#8f8989" },
  { name: "$50 to $100", color: "#8f8989" },
  { name: "$100 and above", color: "#8f8989" },
];

// const initialFacts = [
//   {
//     id: 1,
//     name: "Satin Hydrating Lipstick",
//     source:
//       "https://www.sephora.com/product/satin-hydrating-lipstick-P501496?skuId=2564540&icid2=products%20grid:p501496:product",
//     colorCat: "red",
//     benefitCat: ["Hydrating"],
//     priceCat: "Under $25",
//     price: "$15",
//     imagePath:
//       "https://www.sephora.com/productimages/sku/s2511335-main-zoom.jpg?imwidth=315",
//     score: 1,
//     // votesInteresting: 24,
//     // votesMindblowing: 9,
//     // votesFalse: 4,
//     // createdIn: 2021,
//   },
//   {
//     // id: 2,
//     name: "Forget the Filler Lip-Plumping Line-Smoothing Satin Cream Lipstick",
//     source:
//       "https://www.sephora.com/product/forget-filler-lip-plumping-line-smoothing-satin-cream-lipstick-P506812?skuId=2694552&icid2=products%20grid:p506812:product",
//     colorCat: "pink",
//     benefitCat: ["Plumping"],
//     priceCat: "$25 to $50",
//     price: "$28",
//     imagePath: "lipsticks/2.png",
//     score: 2,
//   },
//   {
//     // id: 3,
//     name: "Matte Velvet Lipstick",
//     source:
//       "https://www.sephora.com/product/matte-velvet-lipstick-P506548?skuId=2666857&icid2=products%20grid:p506548:product",
//     colorCat: "orange",
//     benefitCat: ["Long-wearing"],
//     priceCat: "Under $25",
//     price: "$15",
//     imagePath: "lipsticks/3.png",
//     score: 3,
//     // votesInteresting: 8,
//     // votesMindblowing: 3,
//     // votesFalse: 1,
//     // createdIn: 2015,
//   },
// ];

const all_colors = [
  "pink",
  "orange",
  "red",
  "mauve",
  "plum",
  "coral",
  "terra cotta",
  "brown",
  "berry",
  "natural",
];
const all_benefits = [
  "Hydrating",
  "Long-wearing",
  "Plumping",
  "Transfer-resistant",
  "Transfer-proof",
  "Waterproof",
];

const all_prices = ["Under $25", "$25 to $50", "$50 to $100", "$100 and above"];

function App() {
  const [showForm, setShowForm] = useState(false);
  const [facts, setFacts] = useState(initialFacts);
  const [isLoading, setIsLoading] = useState(false);
  const [currentColor, setCurrentColor] = useState(all_colors);
  const [showColorFilter, setShowColorFilter] = useState(false);
  const [currentBenefit, setCurrentBenefit] = useState(all_benefits);
  const [showBenefitFilter, setShowBenefitFilter] = useState(false);
  const [currentPrice, setCurrentPrice] = useState(all_prices);
  const [showPriceFilter, setShowPriceFilter] = useState(false);

  useEffect(
    function () {
      async function getFacts() {
        setIsLoading(true);
        // let query = supabase.from("facts").select("*");
        // if (currentCatgory !== "all")
        //   query = query.eq("category", currentCatgory);
        // const { data: facts, error } = await query
        //   .order("votesInteresting", { ascending: false })
        //   .limit(1000);

        // if (!error) setFacts(facts);
        // else alert("There was a problem getting data");

        var filteredFacts = initialFacts;
        if (currentColor.length !== 0) {
          filteredFacts = initialFacts.filter((fact) =>
            currentColor.includes(fact.colorCat)
          );
        }
        if (currentBenefit.length !== 0) {
          filteredFacts = filteredFacts.filter((fact) =>
            fact.benefitCat.some((beneift) => currentBenefit.includes(beneift))
          );
        }
        if (currentPrice.length !== 0) {
          filteredFacts = filteredFacts.filter((fact) =>
            currentPrice.includes(fact.priceCat)
          );
        }
        console.log(currentColor);
        console.log(currentBenefit);
        console.log(currentPrice);
        const sortedfacts = filteredFacts.sort((a, b) => b.score - a.score);

        if (
          currentColor.length === all_colors.length &&
          currentBenefit.length === all_benefits.length &&
          currentPrice.length === all_prices.length
        ) {
          setFacts(sortedfacts);
        } else {
          setFacts(sortedfacts.slice(0, 30));
          console.log(sortedfacts.slice(0, 30));
        }

        setIsLoading(false);
      }
      getFacts();
    },
    [currentColor, currentBenefit, currentPrice]
  );

  return (
    <>
      <Header showForm={showForm} setShowForm={setShowForm} />

      {/* {showForm ? (
        <NewFactForm setFacts={setFacts} setShowForm={setShowForm} />
      ) : null} */}
      {showForm ? <UserGuide /> : null}

      <main className="main">
        <aside>
          <PriceFilter
            setCurrentPrice={setCurrentPrice}
            showPriceFilter={showPriceFilter}
            setShowPriceFilter={setShowPriceFilter}
            currentPrice={currentPrice}
          />
          <BenefitFilter
            setCurrentBenefit={setCurrentBenefit}
            showBenefitFilter={showBenefitFilter}
            setShowBenefitFilter={setShowBenefitFilter}
            currentBenefit={currentBenefit}
          />
          <ColorFilter
            setCurrentColor={setCurrentColor}
            showColorFilter={showColorFilter}
            setShowColorFilter={setShowColorFilter}
            currentColor={currentColor}
          />
        </aside>
        {isLoading ? (
          <Loader />
        ) : (
          <FactList facts={facts} setFacts={setFacts} />
        )}
      </main>
    </>
  );
}

function Loader() {
  return <p className="message">Loading ...</p>;
}

function Header({ showForm, setShowForm }) {
  const appTitle = "Lipstick Expert";
  return (
    <header className="header">
      <div className="logo">
        <img
          src="lipstick_finall.png"
          height="68"
          width="68"
          alt="Lipstick Expert Logo"
        />
        <h1>{appTitle}</h1>
      </div>
      <button
        className="btn btn-large btn-open"
        style={{ backgroundImage: "none", backgroundColor: "#bb5105" }}
        onClick={() => setShowForm((show) => !show)}
      >
        {showForm ? "Close" : "User Guide"}
      </button>
    </header>
  );
}

function isValidHttpUrl(string) {
  let url;
  try {
    url = new URL(string);
  } catch (_) {
    return false;
  }
  return url.protocol === "http:" || url.protocol === "https:";
}

function UserGuide() {
  // function NewFactForm({ setFacts, setShowForm }) {
  // re
  // const [text, setText] = useState("");
  // const [source, setSource] = useState("http://example.com");
  // const [category, setCategory] = useState("");
  // const [isUpLoading, setIsUpLoading] = useState(false);
  // const textLength = text.length;

  // async function handleSubmit(e) {
  //1. Prevent browser reload
  // e.preventDefault();
  // console.log(text, source, category);

  //2. Check if data is valid. If so, create a new fact
  // if (text && isValidHttpUrl(source) && category && textLength <= 200)
  //   console.log("there is valid data");

  //3. Create a new fact object
  // const newFact = {
  //   id: Math.round(Math.random() * 1000000000),
  //   text,
  //   source,
  //   category,
  //   votesInteresting: 0,
  //   votesMindblowing: 0,
  //   votesFalse: 0,
  //   createdIn: new Date().getFullYear(),
  // };

  //3. Upload Facts to Supabase and receive the new fact object
  // setIsUpLoading(true);
  // const { data: newFact, error } = await supabase
  //   .from("facts")
  //   .insert([{ text, source, category }])
  //   .select();
  // setIsUpLoading(false);

  //4. Add the new fact to the UI: add the fact to state
  // if (!error) setFacts((facts) => [newFact[0], ...facts]);

  //5. Reset input fields
  // setText("");
  // setSource("");
  // setCategory("");

  //6. Close the form
  // setShowForm(false);
  // }

  return (
    <div className="fact-form">
      <p>
        Adjust FILTERS to get lipstick most popular and suitable for you! Have
        Fun! 🤩
      </p>
    </div>
    // <form className="fact-form" onSubmit={handleSubmit}>
    //   <input
    //     type="text"
    //     placeholder="Share a fact with the world..."
    //     value={text}
    //     onChange={(e) => setText(e.target.value)}
    //     disabled={isUpLoading}
    //   />
    //   <span>{200 - textLength}</span>
    //   <input
    //     type="text"
    //     placeholder="Trustworthy source..."
    //     value={source}
    //     onChange={(e) => setSource(e.target.value)}
    //     disabled={isUpLoading}
    //   />
    //   <select
    //     value={category}
    //     onChange={(e) => setCategory(e.target.value)}
    //     disabled={isUpLoading}
    //   >
    //     <option>Choose category:</option>
    //     {COLOR_CATEGORIES.map((cat) => (
    //       <option key={cat.name} value={cat.name}>
    //         {cat.name.toUpperCase()}
    //       </option>
    //     ))}
    //   </select>
    //   <button className="btn btn-large" disabled={isUpLoading}>
    //     Post
    //   </button>
    // </form>
  );
}

function ColorFilter({
  setCurrentColor,
  showColorFilter,
  setShowColorFilter,
  currentColor,
}) {
  return (
    <ul>
      <li className="category">
        <button
          className="btn btn-all-categories"
          onClick={() => {
            if (showColorFilter) {
              setCurrentColor(all_colors);
            } else {
              setCurrentColor([]);
            }

            setShowColorFilter(!showColorFilter);
          }}
        >
          {showColorFilter ? "All Colors" : "Choose Color"}
        </button>
      </li>

      {showColorFilter ? (
        <div className="color-categories">
          {COLOR_CATEGORIES.map((cat) => (
            <li key={cat.name} className="category">
              <button
                className="btn btn-category"
                style={{
                  backgroundColor: cat.color,
                  border: currentColor.includes(cat.name)
                    ? "3px solid white"
                    : "none",
                }}
                onClick={() => {
                  setCurrentColor((colors) => {
                    if (colors.includes(cat.name)) {
                      // console.log(colors);
                      // If the color is already in the list, return the current list without modification
                      // if (colors.length === all_colors.length) {
                      //   return [cat.name];
                      // }
                      // if (colors.length === 1) {
                      //   return all_colors;
                      // }
                      return colors.filter((color) => color !== cat.name);
                    } else {
                      // If the color is not in the list, return a new array with the added color
                      return [...colors, cat.name];
                    }
                  });
                }}
              >
                {cat.name}
              </button>
            </li>
          ))}
        </div>
      ) : null}
      <div className="divider"></div>
    </ul>
  );
}

function PriceFilter({
  setCurrentPrice,
  showPriceFilter,
  setShowPriceFilter,
  currentPrice,
}) {
  return (
    <ul>
      <li className="category">
        <button
          className="btn btn-all-categories"
          style={{ backgroundImage: "none", backgroundColor: "#8f8989" }}
          onClick={() => {
            if (showPriceFilter) {
              setCurrentPrice(all_prices);
            } else {
              setCurrentPrice([]);
            }

            setShowPriceFilter(!showPriceFilter);
          }}
        >
          {showPriceFilter ? "All Prices" : "Choose Price"}
        </button>
      </li>

      {showPriceFilter ? (
        <div className="color-categories">
          {PRICE_CATEGORIES.map((cat) => (
            <li key={cat.name} className="category">
              <button
                className="btn btn-category"
                style={{
                  backgroundColor: cat.color,
                  border: currentPrice.includes(cat.name)
                    ? "3px solid white"
                    : "none",
                }}
                onClick={() => {
                  setCurrentPrice((prices) => {
                    if (prices.includes(cat.name)) {
                      // console.log(colors);
                      // If the color is already in the list, return the current list without modification
                      // if (colors.length === all_colors.length) {
                      //   return [cat.name];
                      // }
                      // if (colors.length === 1) {
                      //   return all_colors;
                      // }
                      return prices.filter((price) => price !== cat.name);
                    } else {
                      // If the color is not in the list, return a new array with the added color
                      return [...prices, cat.name];
                    }
                  });
                }}
              >
                {cat.name}
              </button>
            </li>
          ))}
        </div>
      ) : null}
      <div className="divider"></div>
    </ul>
  );
}

function BenefitFilter({
  setCurrentBenefit,
  showBenefitFilter,
  setShowBenefitFilter,
  currentBenefit,
}) {
  return (
    <ul>
      <li className="category">
        <button
          className="btn btn-all-categories"
          style={{ backgroundImage: "none", backgroundColor: "#5c35c6" }}
          onClick={() => {
            if (showBenefitFilter) {
              setCurrentBenefit(all_benefits);
            } else {
              setCurrentBenefit([]);
            }

            setShowBenefitFilter(!showBenefitFilter);
          }}
        >
          {showBenefitFilter ? "All Benefits" : "Choose Benefit"}
        </button>
      </li>
      {showBenefitFilter ? (
        <div className="color-categories">
          {BENEFIT_CATEGORIES.map((cat) => (
            <li key={cat.name} className="category">
              <button
                className="btn btn-category"
                style={{
                  backgroundColor: cat.color,
                  border: currentBenefit.includes(cat.name)
                    ? "3px solid white"
                    : "none",
                }}
                onClick={() => {
                  setCurrentBenefit((benefits) => {
                    if (benefits.includes(cat.name)) {
                      // console.log(colors);
                      // If the color is already in the list, return the current list without modification
                      // if (colors.length === all_colors.length) {
                      //   return [cat.name];
                      // }
                      // if (colors.length === 1) {
                      //   return all_colors;
                      // }
                      return benefits.filter((benefit) => benefit !== cat.name);
                    } else {
                      // If the color is not in the list, return a new array with the added color
                      return [...benefits, cat.name];
                    }
                  });
                }}
              >
                {cat.name}
              </button>
            </li>
          ))}
        </div>
      ) : null}
      <div className="divider"></div>
    </ul>
  );
}

function FactList({ facts, setFacts }) {
  if (facts.length === 0) {
    return (
      <p className="message">
        No lipsticks available now! Try something different! 🔥
      </p>
    );
  }

  return (
    <section>
      <ul className="facts-list">
        {facts.map((fact) => (
          <Fact key={fact.source} fact={fact} setFacts={setFacts} />
        ))}
      </ul>
      <p>There are {facts.length} lipsticks for recommendation!</p>
    </section>
  );
}

function Fact({ fact, setFacts }) {
  const [isUpdating, setIsUpdating] = useState(false);
  // const isDisputed =
  //   fact.votesInteresting + fact.votesMindblowing < fact.votesFalse;
  // async function handleVote(columnName) {
  //   setIsUpdating(true);
  // const { data: updatedFact, error } = await supabase
  //   .from("facts")
  //   .update({ [columnName]: fact[columnName] + 1 })
  //   .eq("id", fact.id)
  //   .select();
  // if (!error)
  //   setFacts((facts) =>
  //     facts.map((f) => (f.id === fact.id ? updatedFact[0] : f))
  //   );
  //   setIsUpdating(false);
  // }

  return (
    <li className="fact">
      <div className="image-container" style={{ flex: "0 0 10%" }}>
        <img src={fact.imagePath} className="bordered-image" alt="Lipstick" />
      </div>
      <div className="description" style={{ flex: "0 0 75%" }}>
        <p className="lipstick-name">
          {/* {isDisputed ? <span className="disputed">[⛔️DISPUTED]</span> : null} */}
          {fact.name}
          <a className="source" href={fact.source} target="_blank">
            (Source)
          </a>
        </p>
        <div className="divider-name"></div>
        <div className="des-tags">
          <p>Color: </p>
          <div className="tags">
            {/* <span
              className="tag"
              style={{
                backgroundColor: COLOR_CATEGORIES.find(
                  (cat) => cat.name === fact.colorCat
                ).color,
              }}
            >
              {fact.colorCat}
            </span> */}
          </div>
          <img
            src={fact.colorImg}
            className="bordered-color-image"
            alt="Lipstick"
          />
        </div>
        <div className="des-tags">
          <p>Benefits: </p>
          <div className="tags">
            {fact.benefitCat.map((benefit) => {
              return (
                <span
                  className="tag"
                  style={{
                    backgroundColor: BENEFIT_CATEGORIES.find(
                      (cat) => cat.name === benefit
                    ).color,
                  }}
                >
                  {benefit}
                </span>
              );
            })}
          </div>
        </div>
      </div>
      <p className="lipstick-price" style={{ flex: "0 0 15%" }}>
        {fact.price}
      </p>
      {/* <div className="vote-buttons">
        <button
          onClick={() => handleVote("votesInteresting")}
          disabled={isUpdating}
        >
          👍 {fact.votesInteresting}
        </button>
        <button
          onClick={() => handleVote("votesMindblowing")}
          disabled={isUpdating}
        >
          🤯 {fact.votesMindblowing}
        </button>
        <button onClick={() => handleVote("votesFalse")} disabled={isUpdating}>
          ⛔️ {fact.votesFalse}
        </button>
      </div> */}
    </li>
  );
}

export default App;
