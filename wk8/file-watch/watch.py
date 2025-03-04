import inotify.adapters

def main():
  notifier = inotify.adapters.Inotify()

  notifier.add_watch('./target')
  for event in notifier.event_gen(yield_nones=False):
    print(event)

if __name__ == '__main__':
  main()