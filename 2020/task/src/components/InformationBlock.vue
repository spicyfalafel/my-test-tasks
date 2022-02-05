<template>
    <div>
        <table class="inner table table-borderless">
            <tr>
                <td>
                    <div>
                        <h5>Ежемесячный платеж</h5>
                        <h1 id="month_pay">{{month_pay}} ₽</h1>
                    </div>
                </td>
                <td>
                    <div>
                        <h5>Необходимый доход</h5>
                        <h1 id="income">{{income}} ₽</h1>
                    </div>
                </td>
            </tr>
            <tr>
                <td>
                    <div>
                        <h5>Переплата</h5>
                        <h1 id="overpayment">{{overpayment}} ₽</h1>
                    </div>
                </td>
                <td>
                    <div>
                        <h5>Тело кредита</h5>
                        <h1 id="loan_body">{{loan_body}} ₽</h1>
                    </div>
                </td>
            </tr>
        </table>
    </div>
</template>

<script>
    export default {
        name: "InformationBlock",
        props: {
            property_value: {
                required: true,
            },
            initial_fee: {
                required: true,
            },
            credit_term: {
                required: true,
            },
            interest_rate: {
                required: true,
            }
        },
        computed: {

            loan_body: function(){
                let res = this.property_value-this.initial_fee
                if(!res){
                    return 0
                }
                return res
            },
            month_pay: function(){
                let t = this.interest_rate/1200
                let res =  Math.round(this.loan_body*(t + t/(Math.pow((1+t), this.credit_term*12)-1)))
                if(!res){
                    return 0
                }
                return res
            },
            income: function(){
                let res = Math.round(5 * this.month_pay/3)
                if(!res){
                    return 0
                }
                return res
            },
            overpayment: function(){
                let res = Math.round(this.month_pay*this.credit_term*12-this.property_value+this.initial_fee)
                if(!res){
                    return 0
                }
                return res
            }
        }
    }
</script>

<style scoped>
    .inner {
        background: rgb(235, 235, 235);
        border-radius: 12px;
    }
</style>