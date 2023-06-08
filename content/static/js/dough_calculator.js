

function calcDough() {
    // Read all the HTML input elements
    this.balls = ReadInputs("balls")
    this.ballWeight = ReadInputs("dough_weight")
    this.flour1 = ReadInputs("flour_1")
    this.water = ReadInputs("water")
    this.salt = ReadInputs("salt")
    this.yeast = ReadInputs("yeast")
    this.oil = ReadInputs("oil")
    this.sugar = ReadInputs("sugar")

    // Do some calculations
    this.totalWeight = this.balls * this.ballWeight
    this.allPercents = this.flour1 + this.water + this.salt + this.yeast + this.oil + this.sugar

    // Update outputs
    Outputs("flour_1_wt", (this.flour1 * this.totalWeight / this.allPercents))
    Outputs("water_wt", (this.water * this.totalWeight / this.allPercents))
    Outputs("salt_wt", (this.salt * this.totalWeight / this.allPercents))
    Outputs("yeast_wt", (this.yeast * this.totalWeight / this.allPercents) * (2 / 6))
    Outputs("oil_wt", (this.oil * this.totalWeight / this.allPercents))
    Outputs("sugar_wt", (this.sugar * this.totalWeight / this.allPercents))

}

function Outputs(ingredient, amount) {
    document.getElementById(ingredient).innerText = Round(amount)
}

function Round(n) {
    return (n).toLocaleString("en-US", { minimumFractionDigits: 1, maximumFractionDigits: 1 })
}

function ReadInputs(ingredient) {
    var p = document.getElementById(ingredient).value
    return parseFloat(p)
}

function ShowRecipe(balls, dough_weight, flour_1, water, salt, yeast, oil, sugar) {
    SetValue("balls", balls)
    SetValue("dough_weight", dough_weight)
    SetValue("flour_1", flour_1)
    SetValue("water", water)
    SetValue("salt", salt)
    SetValue("yeast", yeast)
    SetValue("oil", oil)
    SetValue("sugar", sugar)

    calcDough()
}

function SetValue(ingredient, amount) {
    document.getElementById(ingredient).value = amount
}


calcDough()