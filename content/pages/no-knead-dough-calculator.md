---
Title: No-knead dough calculator
---

<link rel="stylesheet" href="/static/css/dough_calculator.css">

<p class="summary">
    Common dough recipes I use:
<ul>
    <li>
        Original Dough in 5 min a day:
        <a href="javascript:ShowRecipe(1, 1617, 100, 75, 2, 1, 0, 0);">1,617 grams</a>
    </li>
    <li>
        Half sheet pan pizza:
        <a href="javascript:ShowRecipe(1, 950, 100, 75, 2, 1, 2, 2);">950 grams</a>
    </li>
    <li>
        Rolls:
        <a href="javascript:ShowRecipe(9, 55, 100, 60, 2, 1, 15, 2);">60 grams</a>
    </li>
</ul>
</p>
<div class="printable">
    <h2 style="text-align:center">Dough calculator</h2>
    <table>
        <tr>
            <th>
                Ingredient
            </th>
            <th>
                %
            </th>
            <th class="weight">
                Weight (grams)
            </th>
        </tr>
        <tr>
            <td>
                <label>Dough Balls</label>
            </td>
            <td>
                <input type="number" min=0 value=1 step=1 id="balls" oninput="calcDough()">
            </td>
        </tr>
        <tr>
            <td>
                <label>Dough Weight<br>(grams)</label>
            </td>
            <td>
                <input type="number" min=1 value=950 step=1 id="dough_weight" oninput="calcDough()">
            </td>
        </tr>
        <tr>
            <td>
                <label>Flour 1</label>
            </td>
            <td>
                <input type="number" id="flour_1" min=100 max=100 value=100 step=1 oninput="calcDough()">
            </td>
            <td class="weight">
                <span id="flour_1_wt"></span>
            </td>
        </tr>
        <tr>
            <td>
                <label>Water</label>
            </td>
            <td>
                <input type="number" min=25 value=75 step=.1 id="water" oninput="calcDough()">
            </td>
            <td class="weight">
                <span id="water_wt"></span>
            </td>
        </tr>
        <tr>
            <td>
                <label>Salt</label>
            </td>
            <td>
                <input type="number" min=0 value=2.0 step=0.1 id="salt" oninput="calcDough()">
            </td>
            <td class="weight">
                <span id="salt_wt"></span>
            </td>
        </tr>
        <tr>
            <td>
                <label>Instant Yeast</label>
            </td>
            <td>
                <input type="number" min=0 value=.9 step=0.01 id="yeast" oninput="calcDough()">
            </td>
            <td class="weight">
                <span id="yeast_wt"></span> tsp
            </td>
        </tr>
        <tr>
            <td>
                <label>Oil</label>
            </td>
            <td>
                <input type="number" min=0 value=0 step=.1 id="oil" oninput="calcDough()">
            </td>
            <td class="weight">
                <span id="oil_wt"></span>
            </td>
        </tr>
        <tr>
            <td>
                <label>Sugar</label>
            </td>
            <td>
                <input type="number" min=0 value=0 step=.1 id="sugar" oninput="calcDough()">
            </td>
            <td class="weight">
                <span id="sugar_wt"></span>
            </td>
        </tr>
    </table>
</div>


<script src="/static/js/dough_calculator.js"></script>