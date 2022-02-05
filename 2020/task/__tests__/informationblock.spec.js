import {mount, createLocalVue } from '@vue/test-utils'
import InformationBlock from "@/components/InformationBlock";


const localVue = createLocalVue()
const property_value = 20000000
const initial_fee = 3000000
const credit_term = 10
const interest_rate = 10

describe('InformationBlock', () => {
    it('computes right data', () => {
        const wrapper = mount(InformationBlock, {localVue,
            propsData: {
                property_value: property_value,
                initial_fee: initial_fee,
                credit_term: credit_term,
                interest_rate: interest_rate
        }})
        const pay = '224656 ₽'
        const two = '374427 ₽'
        const three = '9958720 ₽' //it's 9958750 on pic but I think this is mistake
        const four = '17000000 ₽'

        expect(wrapper.find('#month_pay').text()).toEqual(pay)
        expect(wrapper.find('#income').text()).toEqual(two)
        expect(wrapper.find('#overpayment').text()).toEqual(three)
        expect(wrapper.find('#loan_body').text()).toEqual(four)
    })
})

