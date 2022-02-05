<template>
    <form class="parent">
        <div>
            <div class="form-group">
                <label class="my-label" for="property_value">Стоимость недвижимости (₽)</label>
                <input type="number" class="form-control" @change="connectPropertyValueAndInitialFee"
                       id="property_value" v-model.number="property_value">
            </div>

            <div class="form-group">
                <label class="my-label" for="initial_fee">Первоначальный взнос (₽)</label>
                <input type="number" class="form-control" @change="connectInitialFeeAndPropertyValue" id="initial_fee"
                       v-model.number="initial_fee">
            </div>
            <div class="container">
                <div class="button-wrap">
                    <input id="per10" class="hidden radio-label maybe-button" @click="disableAllPercents"
                           @change="connectPropertyValueAndInitialFee"
                           value="10" v-model="percents" type="radio" name="accept-offers" checked="checked"/>
                    <label class="button-label" for="per10">
                        <h1>10%</h1>
                    </label>
                    <input id="per15" class="hidden radio-label maybe-button" @click="disableAllPercents"
                           @change="connectPropertyValueAndInitialFee"
                           value="15" v-model="percents" type="radio" name="accept-offers"/>
                    <label class="button-label" for="per15">
                        <h1>15%</h1>
                    </label>
                    <input id="per20" class="hidden radio-label maybe-button" @click="disableAllPercents"
                           @change="connectPropertyValueAndInitialFee"
                           value="20" v-model="percents" type="radio" name="accept-offers"/>
                    <label class="button-label" for="per20">
                        <h1>20%</h1>
                    </label>
                    <input id="per25" class="hidden radio-label maybe-button" @click="disableAllPercents"
                           @change="connectPropertyValueAndInitialFee"
                           value="25" v-model="percents" type="radio" name="accept-offers"/>
                    <label class="button-label" for="per25">
                        <h1>25%</h1>
                    </label>
                    <input id="per30" class="hidden radio-label maybe-button" @click="disableAllPercents"
                           @change="connectPropertyValueAndInitialFee"
                           value="30" v-model="percents" type="radio" name="accept-offers"/>
                    <label class="button-label" for="per30">
                        <h1>30%</h1>
                    </label>
                </div>

            </div>

            <div class="form-group">
                <label class="my-label" for="credit_term">Срок кредита (кол-во лет)</label>
                <input type="number" class="form-control" id="credit_term" v-model.number="credit_term">
            </div>

            <div class="form-group">
                <label class="my-label" for="interest_rate">Процентная ставка (%)</label>
                <input type="number" class="form-control" id="interest_rate" v-model.number="interest_rate">
            </div>
            <div class="d-inline-flex">
                <b-button class="my-button" @click="save" id="savebutt">Save</b-button>
                <b-button class="my-button" @click="clear" id="clearbutt">Clear</b-button>
            </div>
        </div>
        <information-block :property_value="property_value"
                           :initial_fee="initial_fee"
                           :credit_term="credit_term"
                           :interest_rate="interest_rate"/>
    </form>
</template>

<script>
    import InformationBlock from "@/components/InformationBlock";

    export default {
        name: "CreditForm",
        components: {InformationBlock},
        data() {
            return {
                property_value: localStorage.getItem('property_value'),
                initial_fee: localStorage.getItem('initial_fee'),
                credit_term: localStorage.getItem('credit_term'),
                interest_rate: localStorage.getItem('interest_rate'),
                percents: localStorage.getItem('percents')
            }
        },
        methods: {
            save: function () {
                localStorage.setItem('property_value', this.property_value)
                localStorage.setItem('initial_fee', this.initial_fee)
                localStorage.setItem('credit_term', this.credit_term)
                localStorage.setItem('interest_rate', this.interest_rate)
                localStorage.setItem('percents', this.percents)
            },
            clear: function () {
                this.property_value = 0
                this.initial_fee = 0
                this.credit_term = 0
                this.interest_rate = 0
            },
            disableAllPercents: function () {
                this.percents = NaN
            },
            connectPropertyValueAndInitialFee: function () {
                if (this.percents) {
                    this.initial_fee = this.property_value * this.percents / 100
                }
            },
            /*numberWithSpaces: function(x) {
                return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
            },*/
            connectInitialFeeAndPropertyValue: function () {
                if (this.percents) {
                    this.property_value = this.initial_fee / this.percents * 100
                }
            }
        },
        /*filters: {
            splitNumber(value) {
                return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
            }
        }*/
    }
</script>


<style scoped>
    #savebutt {
        background-color: limegreen;
    }

    #clearbutt {
        background-color: white;
        color: dimgrey;
    }

    .my-button {
        width: 150px;
        margin-right: 10px;
    }

    .parent {
        display: flex;
        flex-direction: row;
    }

    .parent > * {
        margin: 30px 30px;
    }

    /* https://codepen.io/mblode/pen/gGIAm/ */
    @import url(https://fonts.googleapis.com/css?family=Lato:300,400,900);
    * {
        box-sizing: border-box;
    }

    html, body {
        height: 100%;
    }

    html {
        background: #444;
    }

    body {
        min-height: 100%;
        overflow: hidden;
    }

    .container {
        height: 25%;
        min-height: 25%;
    }

    .button-wrap {
        position: relative;
        text-align: center;
        top: 50%;
        margin-top: -3.5em;
    }

    @media (max-width: 40em) {
        .button-wrap {
            margin-top: -1.5em;
        }
    }

   .my-label{
        text-align: left;
   }

    .button-label {
        display: inline-block;
        padding: 0.3em 0.6em;
        margin: 0.5em;
        cursor: pointer;
        color: #292929;
        border-radius: 0.25em;
        background: #efefef;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2), inset 0 -3px 0 rgba(0, 0, 0, 0.22);
        -webkit-transition: 0.3s;
        transition: 0.3s;
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
    }

    .button-label h1 {
        font-size: 1em;
        font-family: "Lato", sans-serif;
    }

    .button-label:hover {
        background: #d6d6d6;
        color: #101010;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2), inset 0 -3px 0 rgba(0, 0, 0, 0.32);
    }

    .button-label:active {
        -webkit-transform: translateY(2px);
        transform: translateY(2px);
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2), inset 0px -1px 0 rgba(0, 0, 0, 0.22);
    }

    @media (max-width: 40em) {
        .button-label {
            padding: 0em 1em 3px;
            margin: 0.25em;
        }
    }

    .maybe-button:checked + .button-label {
        background: #4183D7;
        color: #efefef;
    }

    .maybe-button:checked + .button-label:hover {
        background: #2c75d2;
        color: #e2e2e2;
    }

    .hidden {
        display: none;
    }

</style>