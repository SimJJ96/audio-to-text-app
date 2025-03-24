import { describe, it, expect } from 'vitest'

import { mount } from '@vue/test-utils';
import QueryTranscription from '../QueryTranscription.vue';

describe('QueryTranscription.vue', () => {
  it('emits the search event when the search button is clicked', async () => {
    const wrapper = mount(QueryTranscription)
    const input = wrapper.find('.search-input')
    const button = wrapper.find('button')

    // Set a value in the input
    await input.setValue('test-file.mp3')

    // Click the search button
    await button.trigger('click')

    // Check if the search event was emitted with the correct value
    expect(wrapper.emitted('search')).toBeTruthy()
    expect(wrapper.emitted('search')[0]).toEqual(['test-file.mp3'])
  })
})