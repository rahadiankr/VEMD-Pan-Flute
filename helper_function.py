import streamlit as st
class fixing_duration:
  def non_negative(base_note):
    temp = 0
    result = []
    for index, item in enumerate(base_note):
      if item[0] < temp:
        if item[1] - temp <= 0:
          result.append((temp, temp, item[2], item[3]))
          temp = temp
        else:
          result.append((temp, item[1], item[2], item[3]))
          temp = item[1]
      else:
        result.append(item)
        temp = item[1]

    return result

class adjusting_notes:
  def transpose_notes(note_events):
    groups = {
      "oktaf_0": (12, 24),
      "oktaf_1": (24, 36),
      "oktaf_2": (36, 48),
      "oktaf_3": (48, 60),
      "oktaf_4": (60, 72),
      "oktaf_5": (72, 84),
      "oktaf_6": (84, 96),
      "oktaf_7": (96, 108),
      "oktaf_8": (108, 120)}

    # Initialize counters for each group
    group_counts = {key: 0 for key in groups}

    # Iterate through the dataset and count the members in each group
    for record in note_events:
      value = record[2]
      for group_name, (lower_bound, upper_bound) in groups.items():
        if lower_bound <= value < upper_bound:
          group_counts[group_name] += 1
          break

    # Sorting using sorted() method
    sorted_dict = {key: value for key, value in sorted(group_counts.items(), key=lambda item: item[1], reverse=True)}

    top_4 = [key for key, value in sorted(group_counts.items(), key=lambda item: item[1], reverse=True)[:4]]
    top_4.sort(reverse=False)
    low_key = top_4[:1]
    middle_key = top_4[1:3]
    high_key = top_4[3:]

    # Initialize a dictionary to hold the grouped data
    grouped_data = {key: [] for key in groups.keys()}

    # Loop through the song data
    for song in note_events:
      # Get the frequency of the song
      frequency = song[2]

      # Loop through the groups to find where the frequency fits
      for group, (lower, upper) in groups.items():
        if lower <= frequency < upper:
          # Add the song to the corresponding group
          grouped_data[group].append(song)
          break

    # Now, grouped_data contains the song data grouped by the specified groups

    # Select the groups from grouped_data that are in list_group
    selected_groups = {key: grouped_data[key] for key in top_4 if key in grouped_data}

    # Now, selected_groups contains the groups from grouped_data that are in list_group

    low = selected_groups[low_key[0]]
    middle = [selected_groups[key] for key in middle_key]
    middle = [item for sublist in middle for item in sublist]
    high = selected_groups[high_key[0]]

    low_low = groups[low_key[0]][0]
    middle_low = groups[middle_key[0]][0]
    high_low = ((groups[high_key[0]][0]) - 12)
    low_reduced = [(item[0], item[1], item[2] - low_low, item[3]) for item in low]
    mid_reduced = [(item[0], item[1], item[2] - middle_low, item[3]) for item in middle]
    high_reduced = [(item[0], item[1], item[2] - high_low, item[3]) for item in high]
    reduced = low_reduced + mid_reduced + high_reduced
    # reduced = mid_reduced
    # st.write(len(low_reduced))
    # st.write(len(mid_reduced))
    # st.write(len(high_reduced))
    # st.write(len(reduced))

    return reduced

  def adjust_notes(fix_duration):
    kress_notes = [1, 3, 6, 8, 10, 13, 15, 18, 20, 22]
    notes_to_flute = {-1: 1, 0: 2, 2: 3, 4: 4, 5: 5, 7: 6, 9: 7, 11: 8, 12: 9, 14: 10, 16: 11, 17: 12, 19: 13, 21: 14,
                      23: 15, 24: 16}

    for index, item in enumerate(fix_duration):
      # eliminated_kress_notes = [(item[0], item[1], item[2]-1 if item[2] in kress_notes else item[2], item[3]) for item in fix_duration]
      eliminated_kress_notes = [item for item in fix_duration if item[2] not in kress_notes]

    adjusted_notes = [(item[0], item[1], notes_to_flute[item[2]] if item[2] in notes_to_flute else None, item[3]) for
                      item in eliminated_kress_notes]
    return adjusted_notes