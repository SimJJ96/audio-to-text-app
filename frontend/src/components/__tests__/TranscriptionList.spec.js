import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import TranscriptionList from '../TranscriptionList.vue'

describe('TranscriptionList.vue', () => {
  it('displays transcriptions in the table', () => {
    const transcriptions = [
      { id: 1, file_name: 'file1.mp3', text: 'This is the transcription for file1.' },
      { id: 2, file_name: 'file2.wav', text: 'This is the transcription for file2.' },
    ]

    const wrapper = mount(TranscriptionList, {
      props: {
        transcriptions,
      },
    })

    const rows = wrapper.findAll('tbody tr')
    expect(rows.length).toBe(2)

    // Check the first row
    expect(rows[0].findAll('td')[0].text()).toBe('file1.mp3')
    expect(rows[0].findAll('td')[1].text()).toBe('This is the transcription for file1.')

    // Check the second row
    expect(rows[1].findAll('td')[0].text()).toBe('file2.wav')
    expect(rows[1].findAll('td')[1].text()).toBe('This is the transcription for file2.')
  })
})