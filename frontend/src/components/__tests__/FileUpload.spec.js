import { describe, it, expect } from 'vitest'

import { mount } from '@vue/test-utils'
import FileUpload from '../FileUpload.vue';

describe('FileUpload.vue', () => {
  it('displays an error message for invalid file formats', async () => {
    const wrapper = mount(FileUpload);

    const invalidFile = new File([''], 'invalid-file.txt', { type: 'text/plain' });
    const fileInput = wrapper.find('input[type="file"]')

    Object.defineProperty(fileInput.element, 'files', {
      value: [invalidFile],
    });
    await fileInput.trigger('change')

    expect(wrapper.vm.message).toBe('Invalid file format. Supported formats: .wav, .mp3, .mp4, .m4a, .webm.');
    expect(wrapper.vm.isError).toBe(true);
    expect(wrapper.find('p').text()).toBe('Invalid file format. Supported formats: .wav, .mp3, .mp4, .m4a, .webm.');
    expect(wrapper.find('p').classes()).toContain('error')
  })
})