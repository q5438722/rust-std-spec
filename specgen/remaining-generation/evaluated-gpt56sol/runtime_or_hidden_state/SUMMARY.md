# Rust std missing-contract generation with determinism feedback

- Model: `gpt-5.6-sol`
- Targets: 495
- Add-spec decisions: 17
- Skip decisions: 478
- Static skips: 0
- Raw determinism reward: 4
- Guarded reward: 0
- LLM errors: 0
- Soundness: external contracts remain unverified; no candidate is automatically eligible for upstream application.

| Target | Category | Decision | Raw | Guarded | Issues |
|---|---|---|---:|---:|---|
| `std::env::args` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::env::args_os` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::env::current_dir` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::env::current_exe` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::env::home_dir` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::env::join_paths` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::env::remove_var` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, no_modeled_observable_output |
| `std::env::set_current_dir` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::env::set_var` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, no_modeled_observable_output |
| `std::env::split_paths` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::env::temp_dir` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::env::var` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::env::var_os` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::env::vars` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::env::vars_os` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::DirBuilder::create` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::DirBuilder::new` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::DirBuilder::recursive` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::DirEntry::file_name` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::DirEntry::file_type` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::DirEntry::metadata` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::DirEntry::path` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::create` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::create_new` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::lock` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::lock_shared` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::metadata` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::open` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::options` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::set_len` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::set_modified` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::set_permissions` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::set_times` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::sync_all` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::sync_data` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::try_clone` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::try_lock` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::try_lock_shared` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::unlock` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::FileTimes::new` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::FileTimes::set_accessed` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::FileTimes::set_modified` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::FileType::is_dir` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::FileType::is_file` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::FileType::is_symlink` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::Metadata::accessed` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::Metadata::created` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::Metadata::file_type` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::Metadata::is_dir` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::Metadata::is_file` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::Metadata::is_symlink` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::Metadata::len` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::Metadata::modified` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::Metadata::permissions` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::OpenOptions::append` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::OpenOptions::create` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::OpenOptions::create_new` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::OpenOptions::new` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::OpenOptions::open` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::OpenOptions::read` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::OpenOptions::truncate` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::OpenOptions::write` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::Permissions::readonly` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::Permissions::set_readonly` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::canonicalize` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::copy` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::create_dir` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::create_dir_all` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::exists` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::hard_link` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::metadata` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::read` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::read_dir` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::read_link` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::read_to_string` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::remove_dir` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::remove_dir_all` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::remove_file` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::rename` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::set_permissions` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::soft_link` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::symlink_metadata` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::write` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufReader::buffer` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufReader::capacity` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufReader::get_mut` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufReader::get_ref` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufReader::into_inner` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufReader::new` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufReader::seek_relative` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufReader::with_capacity` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufWriter::buffer` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufWriter::capacity` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufWriter::get_mut` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufWriter::get_ref` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufWriter::into_inner` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufWriter::into_parts` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufWriter::new` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufWriter::with_capacity` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::IntoInnerError::error` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::IntoInnerError::into_error` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::IntoInnerError::into_inner` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::IntoInnerError::into_parts` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::LineWriter::get_mut` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::LineWriter::get_ref` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::LineWriter::into_inner` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::LineWriter::new` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::LineWriter::with_capacity` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::PipeReader::try_clone` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::PipeWriter::try_clone` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::Stderr::lock` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::Stdin::lines` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::Stdin::lock` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::Stdin::read_line` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::io::Stdout::lock` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::WriterPanicked::into_inner` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::copy` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::pipe` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::read_to_string` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::stderr` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::stdin` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::stdout` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpListener::accept` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpListener::bind` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpListener::incoming` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpListener::local_addr` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpListener::only_v6` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpListener::set_nonblocking` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpListener::set_only_v6` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpListener::set_ttl` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpListener::take_error` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpListener::try_clone` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpListener::ttl` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::connect` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::connect_timeout` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::local_addr` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::nodelay` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::peek` | io_os_runtime | add_spec | 0 | 0 | checker_status:verus_error, classification:runtime_or_hidden_state |
| `std::net::TcpStream::peer_addr` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::read_timeout` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::set_nodelay` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::set_nonblocking` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::set_read_timeout` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::set_ttl` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::set_write_timeout` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::shutdown` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::take_error` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::try_clone` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::ttl` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::write_timeout` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::bind` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::broadcast` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::connect` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::join_multicast_v4` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::join_multicast_v6` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::leave_multicast_v4` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::leave_multicast_v6` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::local_addr` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::multicast_loop_v4` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::multicast_loop_v6` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::multicast_ttl_v4` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::peek` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::peek_from` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::peer_addr` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::read_timeout` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::recv` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::recv_from` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::send` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::send_to` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::set_broadcast` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::set_multicast_loop_v4` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::set_multicast_loop_v6` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::set_multicast_ttl_v4` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::set_nonblocking` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::set_read_timeout` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::set_ttl` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::set_write_timeout` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::take_error` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::try_clone` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::ttl` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::write_timeout` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::fd::BorrowedFd::borrow_raw` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::fd::BorrowedFd::try_clone_to_owned` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::fd::OwnedFd::try_clone` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::fs::chown` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::fs::chroot` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::fs::fchown` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::fs::lchown` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::fs::symlink` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::SocketAddr::as_pathname` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::SocketAddr::from_pathname` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::SocketAddr::is_unnamed` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::bind` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::bind_addr` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::connect` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::connect_addr` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::local_addr` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::pair` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::peer_addr` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::read_timeout` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::recv` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::recv_from` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::send` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::send_to` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::send_to_addr` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::set_nonblocking` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::set_read_timeout` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::set_write_timeout` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::shutdown` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::take_error` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::try_clone` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::unbound` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::write_timeout` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixListener::accept` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixListener::bind` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixListener::bind_addr` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixListener::incoming` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixListener::local_addr` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixListener::set_nonblocking` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixListener::take_error` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixListener::try_clone` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixStream::connect` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixStream::connect_addr` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixStream::local_addr` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixStream::pair` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixStream::peer_addr` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixStream::read_timeout` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixStream::set_nonblocking` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixStream::set_read_timeout` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixStream::set_write_timeout` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixStream::shutdown` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixStream::take_error` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixStream::try_clone` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixStream::write_timeout` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::windows::fs::symlink_dir` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::windows::fs::symlink_file` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::windows::io::BorrowedHandle::borrow_raw` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::windows::io::BorrowedHandle::try_clone_to_owned` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::windows::io::BorrowedSocket::borrow_raw` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::windows::io::BorrowedSocket::try_clone_to_owned` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::windows::io::HandleOrInvalid::from_raw_handle` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::windows::io::HandleOrNull::from_raw_handle` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::windows::io::OwnedHandle::try_clone` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::windows::io::OwnedSocket::try_clone` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Child::id` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Child::kill` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Child::try_wait` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Child::wait` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Child::wait_with_output` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::arg` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::args` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::current_dir` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::env` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::env_clear` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::env_remove` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::envs` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::get_args` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::get_current_dir` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::get_envs` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::get_program` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::new` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::output` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::spawn` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::status` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::stderr` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::stdin` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::stdout` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::ExitStatus::code` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::ExitStatus::success` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Stdio::inherit` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Stdio::null` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Stdio::piped` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::abort` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::exit` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::id` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Barrier::new` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Barrier::wait` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::BarrierWaitResult::is_leader` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Condvar::new` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Condvar::notify_all` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, no_modeled_observable_output |
| `std::sync::Condvar::notify_one` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, no_modeled_observable_output |
| `std::sync::Condvar::wait` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Condvar::wait_timeout` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Condvar::wait_timeout_ms` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Condvar::wait_timeout_while` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Condvar::wait_while` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LazyLock::force` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LazyLock::force_mut` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LazyLock::get` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LazyLock::get_mut` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LazyLock::new` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::and` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::LockResult::and_then` | io_os_runtime | add_spec | 0 | 0 | classification:runtime_or_hidden_state, determinism_not_proved:unknown |
| `std::sync::LockResult::as_deref` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::as_deref_mut` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::as_mut` | io_os_runtime | add_spec | 0 | 0 | classification:runtime_or_hidden_state, determinism_not_proved:unknown, structured_contract_mismatch |
| `std::sync::LockResult::as_ref` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::LockResult::cloned` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::LockResult::copied` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::LockResult::err` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::expect` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::expect_err` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::flatten` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::inspect` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::inspect_err` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::is_err` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::is_err_and` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::is_ok` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::is_ok_and` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::iter` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::iter_mut` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::map` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::map_err` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::map_or` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::map_or_default` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::map_or_else` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::ok` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::or` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::or_else` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::transpose` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::LockResult::unwrap` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::unwrap_err` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::LockResult::unwrap_err_unchecked` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::unwrap_or` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::LockResult::unwrap_or_default` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::LockResult::unwrap_or_else` | io_os_runtime | add_spec | 0 | 0 | classification:runtime_or_hidden_state, determinism_not_proved:unknown |
| `std::sync::LockResult::unwrap_unchecked` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::Mutex::clear_poison` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, no_modeled_observable_output |
| `std::sync::Mutex::get_mut` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Mutex::into_inner` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Mutex::is_poisoned` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Mutex::lock` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Mutex::new` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Mutex::try_lock` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Once::call_once` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, no_modeled_observable_output |
| `std::sync::Once::call_once_force` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, no_modeled_observable_output |
| `std::sync::Once::is_completed` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Once::new` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Once::wait` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, no_modeled_observable_output |
| `std::sync::Once::wait_force` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, no_modeled_observable_output |
| `std::sync::OnceLock::get` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::OnceLock::get_mut` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::OnceLock::get_or_init` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::OnceLock::into_inner` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::OnceLock::new` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::OnceLock::set` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::OnceLock::take` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::OnceLock::wait` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::OnceState::is_poisoned` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::PoisonError::get_mut` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::PoisonError::get_ref` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::PoisonError::into_inner` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::PoisonError::new` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::RwLock::clear_poison` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, no_modeled_observable_output |
| `std::sync::RwLock::get_mut` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::RwLock::into_inner` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::RwLock::is_poisoned` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::RwLock::new` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::RwLock::read` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::RwLock::try_read` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::RwLock::try_write` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::RwLock::write` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::RwLockWriteGuard::downgrade` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::and` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::TryLockResult::and_then` | io_os_runtime | add_spec | 0 | 0 | classification:runtime_or_hidden_state, determinism_not_proved:unknown |
| `std::sync::TryLockResult::as_deref` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::as_deref_mut` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::as_mut` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::as_ref` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::cloned` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::TryLockResult::copied` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::TryLockResult::err` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::expect` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::expect_err` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::flatten` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::inspect` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::inspect_err` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::is_err` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::is_err_and` | io_os_runtime | add_spec | 0 | 0 | classification:runtime_or_hidden_state, determinism_not_proved:unknown |
| `std::sync::TryLockResult::is_ok` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::TryLockResult::is_ok_and` | io_os_runtime | add_spec | 0 | 0 | classification:runtime_or_hidden_state, determinism_not_proved:unknown |
| `std::sync::TryLockResult::iter` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::iter_mut` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::map` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::TryLockResult::map_err` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::TryLockResult::map_or` | io_os_runtime | add_spec | 0 | 0 | classification:runtime_or_hidden_state, determinism_not_proved:unknown |
| `std::sync::TryLockResult::map_or_default` | io_os_runtime | add_spec | 1 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::map_or_else` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::ok` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::TryLockResult::or` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::TryLockResult::or_else` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::TryLockResult::transpose` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::TryLockResult::unwrap` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::unwrap_err` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::unwrap_err_unchecked` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::unwrap_or` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::TryLockResult::unwrap_or_default` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::TryLockResult::unwrap_or_else` | io_os_runtime | add_spec | 0 | 0 | classification:runtime_or_hidden_state, determinism_not_proved:unknown |
| `std::sync::TryLockResult::unwrap_unchecked` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::WaitTimeoutResult::timed_out` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::mpsc::Receiver::iter` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::mpsc::Receiver::recv` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::mpsc::Receiver::recv_timeout` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::mpsc::Receiver::try_iter` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::mpsc::Receiver::try_recv` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::mpsc::Sender::send` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::mpsc::SyncSender::send` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::mpsc::SyncSender::try_send` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::mpsc::channel` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::mpsc::sync_channel` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Builder::name` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Builder::new` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Builder::spawn` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Builder::spawn_scoped` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Builder::spawn_unchecked` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Builder::stack_size` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::JoinHandle::is_finished` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::JoinHandle::join` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::JoinHandle::thread` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::LocalKey::get` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::LocalKey::replace` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::LocalKey::set` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, no_modeled_observable_output |
| `std::thread::LocalKey::take` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::LocalKey::try_with` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::LocalKey::update` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, no_modeled_observable_output |
| `std::thread::LocalKey::with` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::LocalKey::with_borrow` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::LocalKey::with_borrow_mut` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::and` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::thread::Result::and_then` | io_os_runtime | add_spec | 0 | 0 | classification:runtime_or_hidden_state, determinism_not_proved:unknown |
| `std::thread::Result::as_deref` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::as_deref_mut` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::as_mut` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::as_ref` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::thread::Result::cloned` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::thread::Result::copied` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::thread::Result::err` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::thread::Result::expect` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::expect_err` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::thread::Result::flatten` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::thread::Result::inspect` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::thread::Result::inspect_err` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::thread::Result::is_err` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::is_err_and` | io_os_runtime | add_spec | 0 | 0 | classification:runtime_or_hidden_state, determinism_not_proved:unknown |
| `std::thread::Result::is_ok` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::is_ok_and` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::iter` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::iter_mut` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::map` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::map_err` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::map_or` | io_os_runtime | add_spec | 1 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::map_or_default` | io_os_runtime | add_spec | 1 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::map_or_else` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::ok` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::thread::Result::or` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::thread::Result::or_else` | io_os_runtime | add_spec | 0 | 0 | classification:runtime_or_hidden_state, determinism_not_proved:unknown |
| `std::thread::Result::transpose` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::thread::Result::unwrap` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::unwrap_err` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::unwrap_err_unchecked` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::thread::Result::unwrap_or` | io_os_runtime | add_spec | 1 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::unwrap_or_default` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::unwrap_or_else` | io_os_runtime | add_spec | 0 | 0 | classification:runtime_or_hidden_state, determinism_not_proved:unknown |
| `std::thread::Result::unwrap_unchecked` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::thread::Scope::spawn` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::ScopedJoinHandle::is_finished` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::ScopedJoinHandle::join` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::ScopedJoinHandle::thread` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Thread::id` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Thread::name` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Thread::unpark` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, no_modeled_observable_output |
| `std::thread::available_parallelism` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::current` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::panicking` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::park` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, no_modeled_observable_output |
| `std::thread::park_timeout` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, no_modeled_observable_output |
| `std::thread::park_timeout_ms` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, no_modeled_observable_output |
| `std::thread::scope` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::sleep` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, no_modeled_observable_output |
| `std::thread::sleep_ms` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, no_modeled_observable_output |
| `std::thread::spawn` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::yield_now` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, no_modeled_observable_output |
| `std::time::Instant::checked_add` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::time::Instant::checked_duration_since` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::time::Instant::checked_sub` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::time::Instant::duration_since` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::time::Instant::elapsed` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::time::Instant::now` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::time::Instant::saturating_duration_since` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::time::SystemTime::checked_add` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::time::SystemTime::checked_sub` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::time::SystemTime::duration_since` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::time::SystemTime::elapsed` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::time::SystemTime::now` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::time::SystemTimeError::duration` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
