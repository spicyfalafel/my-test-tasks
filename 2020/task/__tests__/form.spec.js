import {mount, createLocalVue } from '@vue/test-utils'
import CreditForm from "@/components/CreditForm";
const localVue = createLocalVue()

describe('CreditForm', () => {
    it('clear function clears fields', () => {
        const wrapper = mount(CreditForm, {localVue})
        wrapper.vm.$emit('clear')
        expect(wrapper.find("#property_value").text()).toEqual('')
        expect(wrapper.find("#initial_fee").text()).toEqual('')
        expect(wrapper.find("#credit_term").text()).toEqual('')
        expect(wrapper.find("#interest_rate").text()).toEqual('')
    })
})

