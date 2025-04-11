from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
from pymysql.cursors import DictCursor
from datetime import datetime
import hashlib
import json
import os
import random
import time

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configuration
DIFFICULTY = 4  # Number of leading zeros required for mining
MINING_REWARD = 1.0  # Reward per block mined

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'voteadmin',
    'password': 'your_secure_password',
    'db': 'blockchain_vote',
    'cursorclass': DictCursor
}

def get_db():
    return pymysql.connect(**db_config)

# Mining Functions
def validate_proof(previous_hash, nonce, difficulty=DIFFICULTY):
    """Validate if the proof meets difficulty requirements"""
    guess = f"{previous_hash}{nonce}".encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:difficulty] == '0' * difficulty

def calculate_hash(block):
    """Calculate SHA-256 hash of a block"""
    block_string = json.dumps(block, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()

def mine_block(block_data, miner_address):
    """Mine a new block with proof-of-work"""
    previous_hash = block_data['previous_hash']
    nonce = 0
    start_time = time.time()

    # Mining process (proof-of-work)
    while not validate_proof(previous_hash, nonce):
        nonce += 1

    mining_time = time.time() - start_time

    # Add mining information to block
    block_data['nonce'] = nonce
    block_data['miner_address'] = miner_address
    block_data['hash'] = calculate_hash(block_data)

    # Save to database
    with get_db() as db:
        with db.cursor() as cur:
            # Insert block
            cur.execute("""
                INSERT INTO blocks (
                    previous_hash, timestamp, proof,
                    voter_id, candidate_id, hash,
                    miner_address, nonce
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                block_data['previous_hash'],
                block_data['timestamp'],
                block_data['proof'],
                block_data['voter_id'],
                block_data['candidate_id'],
                block_data['hash'],
                block_data['miner_address'],
                block_data['nonce']
            ))

            # Update miner's balance
            cur.execute("""
                INSERT INTO miners (address, balance, total_blocks_mined)
                VALUES (%s, %s, 1)
                ON DUPLICATE KEY UPDATE
                    balance = balance + VALUES(balance),
                    total_blocks_mined = total_blocks_mined + 1
            """, (miner_address, MINING_REWARD))

            # Update candidate votes if this is a voting block
            if block_data['candidate_id']:
                cur.execute("""
                    UPDATE candidates
                    SET votes = votes + 1
                    WHERE id = %s
                """, (block_data['candidate_id'],))

            db.commit()

    return mining_time

# Voting Routes
@app.route('/')
def index():
    """Show voting interface"""
    try:
        with get_db() as db:
            with db.cursor() as cur:
                cur.execute("SELECT * FROM candidates WHERE active = TRUE ORDER BY name")
                candidates = cur.fetchall()
        return render_template('index.html', 
                            candidates=candidates,
                            now=datetime.now())  # Explicitly pass now if needed
    except Exception as e:
        app.logger.error(f"Database error in index: {str(e)}")
        flash(f"Database error: {str(e)}", 'error')
        return render_template('index.html', candidates=[])

@app.route('/vote', methods=['POST'])
def vote():
    """Process a vote and mine a block"""
    voter_id = request.form.get('voter_id')
    candidate_id = request.form.get('candidate_id')
    miner_address = request.form.get('miner_address', f"miner_{random.randint(1000,9999)}")

    if not voter_id or not candidate_id:
        flash("Missing voter ID or candidate selection", 'error')
        return redirect(url_for('index'))

    try:
        with get_db() as db:
            with db.cursor() as cur:
                # Check if voter already exists
                cur.execute("SELECT 1 FROM blocks WHERE voter_id = %s", (voter_id,))
                if cur.fetchone():
                    flash("Error: You have already voted!", 'error')
                    return redirect(url_for('index'))

                # Get previous block
                cur.execute("SELECT hash FROM blocks ORDER BY id DESC LIMIT 1")
                last_block = cur.fetchone()
                previous_hash = last_block['hash'] if last_block else "0"  # Genesis block

                # Create block data
                block = {
                    'previous_hash': previous_hash,
                    'timestamp': str(datetime.now()),
                    'proof': 0,  # Will be set during mining
                    'voter_id': voter_id,
                    'candidate_id': candidate_id,
                    'hash': ''  # Will be calculated
                }

                # Mine the block
                mining_time = mine_block(block, miner_address)
                flash(f"Vote recorded! Block mined by {miner_address} in {mining_time:.2f}s", 'success')

    except Exception as e:
        flash(f"Voting error: {str(e)}", 'error')

    return redirect(url_for('results'))

# Mining Routes
@app.route('/miners')
def list_miners():
    """Show miner rankings"""
    try:
        with get_db() as db:
            with db.cursor() as cur:
                cur.execute("SELECT * FROM miners ORDER BY total_blocks_mined DESC, balance DESC")
                miners = cur.fetchall()
        return render_template('miners/list.html', miners=miners)
    except Exception as e:
        flash(f"Database error: {str(e)}", 'error')
        return render_template('miners/list.html', miners=[])


@app.route('/mine', methods=['GET', 'POST'])
def mine():
    """Manual mining interface"""
    if request.method == 'POST':
        miner_address = request.form.get('miner_address', f"miner_{random.randint(1000,9999)}")

        try:
            with get_db() as db:
                with db.cursor() as cur:
                    # Get previous block
                    cur.execute("SELECT hash FROM blocks ORDER BY id DESC LIMIT 1")
                    last_block = cur.fetchone()
                    previous_hash = last_block['hash'] if last_block else "0"

            # Create empty block with dummy voter_id
            block_data = {
                'previous_hash': previous_hash,
                'timestamp': str(datetime.now()),
                'proof': 0,
                'voter_id': 'mining_reward',  # Special value for mined blocks
                'candidate_id': None,
                'hash': ''
            }

            # Mine the block
            mining_time = mine_block(block_data, miner_address)
            flash(f"Block mined by {miner_address} in {mining_time:.2f}s!", 'success')
            return redirect(url_for('list_miners'))

        except Exception as e:
            flash(f"Mining error: {str(e)}", 'error')

    return render_template('miners/mine.html')


# Blockchain Explorer
@app.route('/blockchain')
def blockchain():
    """Show all blocks"""
    try:
        with get_db() as db:
            with db.cursor() as cur:
                cur.execute("""
                    SELECT b.id, b.previous_hash, b.timestamp,
                           b.voter_id, b.candidate_id, b.hash,
                           b.miner_address, b.nonce,
                           c.name AS candidate_name
                    FROM blocks b
                    LEFT JOIN candidates c ON b.candidate_id = c.id
                    ORDER BY b.id
                """)
                blocks = cur.fetchall()
        return render_template('blockchain.html', blocks=blocks)
    except Exception as e:
        flash(f"Database error: {str(e)}", 'error')
        return render_template('blockchain.html', blocks=[])

# Results Route
@app.route('/results')
def results():
    """Show voting results"""
    try:
        with get_db() as db:
            with db.cursor() as cur:
                cur.execute("""
                    SELECT c.id, c.name, c.votes,
                           ROUND(100 * c.votes / NULLIF((SELECT SUM(votes) FROM candidates), 0), 1) as percentage
                    FROM candidates c
                    ORDER BY c.votes DESC
                """)
                candidates = cur.fetchall()

                cur.execute("SELECT COUNT(*) as total FROM blocks WHERE candidate_id IS NOT NULL")
                total = cur.fetchone()
                total_votes = total['total'] if total else 0

        return render_template('results.html',
                            candidates=candidates,
                            total_votes=total_votes)
    except Exception as e:
        flash(f"Database error: {str(e)}", 'error')
        return render_template('results.html', candidates=[], total_votes=0)

# Admin Routes (Candidate Management)
# ... (keep all existing imports and configuration above)

# Admin Routes (Candidate Management)
@app.route('/manage_candidates')
def manage_candidates():
    """Admin interface for managing candidates"""
    try:
        with get_db() as db:
            with db.cursor() as cur:
                cur.execute("SELECT * FROM candidates ORDER BY name")
                candidates = cur.fetchall()
        return render_template('admin/candidates.html', candidates=candidates)
    except Exception as e:
        flash(f"Database error: {str(e)}", 'error')
        return redirect(url_for('index'))

@app.route('/admin/candidates/add', methods=['GET', 'POST'])
def add_candidate():
    """Add a new candidate"""
    if request.method == 'POST':
        name = request.form.get('name')
        if not name:
            flash("Candidate name is required", 'error')
            return redirect(url_for('add_candidate'))

        try:
            with get_db() as db:
                with db.cursor() as cur:
                    # Generate a unique ID
                    cur.execute("SELECT MAX(CAST(id AS UNSIGNED)) as max_id FROM candidates")
                    max_id = cur.fetchone()['max_id']
                    new_id = str(int(max_id) + 1) if max_id else '1'

                    cur.execute(
                        "INSERT INTO candidates (id, name) VALUES (%s, %s)",
                        (new_id, name.strip())
                    )
                    db.commit()
            flash("Candidate added successfully!", 'success')
            return redirect(url_for('manage_candidates'))
        except Exception as e:
            flash(f"Error adding candidate: {str(e)}", 'error')

    return render_template('admin/add_candidate.html')

@app.route('/admin/candidates/edit/<candidate_id>', methods=['GET', 'POST'])
def edit_candidate(candidate_id):
    """Edit an existing candidate"""
    try:
        with get_db() as db:
            with db.cursor() as cur:
                cur.execute("SELECT * FROM candidates WHERE id = %s", (candidate_id,))
                candidate = cur.fetchone()

                if not candidate:
                    flash("Candidate not found", 'error')
                    return redirect(url_for('manage_candidates'))

                if request.method == 'POST':
                    new_name = request.form.get('name')
                    active = request.form.get('active') == 'on'

                    if not new_name:
                        flash("Candidate name is required", 'error')
                    else:
                        cur.execute(
                            "UPDATE candidates SET name = %s, active = %s WHERE id = %s",
                            (new_name.strip(), active, candidate_id)
                        )
                        db.commit()
                        flash("Candidate updated successfully!", 'success')
                        return redirect(url_for('manage_candidates'))

        return render_template('admin/edit_candidate.html', candidate=candidate)
    except Exception as e:
        flash(f"Database error: {str(e)}", 'error')
        return redirect(url_for('manage_candidates'))

@app.route('/admin/candidates/delete/<candidate_id>', methods=['POST'])
def delete_candidate(candidate_id):
    """Delete a candidate (soft delete)"""
    try:
        with get_db() as db:
            with db.cursor() as cur:
                # Check if candidate has votes
                cur.execute("SELECT COUNT(*) as vote_count FROM blocks WHERE candidate_id = %s", (candidate_id,))
                vote_count = cur.fetchone()['vote_count']

                if vote_count > 0:
                    # Can't delete, so deactivate
                    cur.execute(
                        "UPDATE candidates SET active = FALSE WHERE id = %s",
                        (candidate_id,)
                    )
                    db.commit()
                    flash("Candidate has votes and cannot be deleted. Marked as inactive instead.", 'warning')
                else:
                    # No votes, safe to delete
                    cur.execute(
                        "DELETE FROM candidates WHERE id = %s",
                        (candidate_id,)
                    )
                    db.commit()
                    flash("Candidate deleted successfully!", 'success')
    except Exception as e:
        flash(f"Error deleting candidate: {str(e)}", 'error')

    return redirect(url_for('manage_candidates'))

# ... (keep all other existing routes below)

@app.route('/admin/reset_votes.html')
def reset_votes():
    try:
        # Your logic to reset votes (e.g., interacting with blockchain)
        return render_template('reset_votes.html', success=True)
    except Exception as e:
        return f"Error resetting votes: {str(e)}", 500

# Blockchain Explorer Enhanced Routes
@app.route('/block/<string:block_hash>')
def block_detail(block_hash):
    """Show detailed information about a specific block"""
    try:
        with get_db() as db:
            with db.cursor() as cur:
                # Get block details
                cur.execute("""
                    SELECT b.*, c.name AS candidate_name
                    FROM blocks b
                    LEFT JOIN candidates c ON b.candidate_id = c.id
                    WHERE b.hash = %s
                """, (block_hash,))
                block = cur.fetchone()

                if not block:
                    flash("Block not found", 'error')
                    return redirect(url_for('blockchain'))

                # Get previous and next blocks
                cur.execute("""
                    SELECT hash FROM blocks 
                    WHERE id = (SELECT MAX(id) FROM blocks WHERE id < %s)
                """, (block['id'],))
                prev_block = cur.fetchone()

                cur.execute("""
                    SELECT hash FROM blocks 
                    WHERE id = (SELECT MIN(id) FROM blocks WHERE id > %s)
                """, (block['id'],))
                next_block = cur.fetchone()

        return render_template('explorer/block_detail.html',
                            block=block,
                            prev_block=prev_block['hash'] if prev_block else None,
                            next_block=next_block['hash'] if next_block else None)
    except Exception as e:
        flash(f"Error retrieving block: {str(e)}", 'error')
        return redirect(url_for('blockchain'))

@app.route('/address/<string:address>')
def address_detail(address):
    """Show all transactions for a specific address (miner or voter)"""
    try:
        with get_db() as db:
            with db.cursor() as cur:
                # Get blocks mined by this address
                cur.execute("""
                    SELECT * FROM blocks 
                    WHERE miner_address = %s 
                    ORDER BY id DESC
                """, (address,))
                mined_blocks = cur.fetchall()

                # Get votes cast by this address
                cur.execute("""
                    SELECT b.*, c.name AS candidate_name
                    FROM blocks b
                    LEFT JOIN candidates c ON b.candidate_id = c.id
                    WHERE b.voter_id = %s
                    ORDER BY b.id DESC
                """, (address,))
                votes = cur.fetchall()

                # Get miner balance if exists
                cur.execute("""
                    SELECT balance FROM miners WHERE address = %s
                """, (address,))
                miner_data = cur.fetchone()

        return render_template('explorer/address_detail.html',
                            address=address,
                            mined_blocks=mined_blocks,
                            votes=votes,
                            balance=miner_data['balance'] if miner_data else 0)
    except Exception as e:
        flash(f"Error retrieving address data: {str(e)}", 'error')
        return redirect(url_for('blockchain'))

@app.route('/search', methods=['GET'])
def search():
    """Search for blocks, transactions, or addresses"""
    query = request.args.get('q', '').strip()
    if not query:
        return redirect(url_for('blockchain'))

    # Check if it's a block hash (64 chars)
    if len(query) == 64:
        return redirect(url_for('block_detail', block_hash=query))
    # Check if it's an address (starts with "miner_")
    elif query.startswith('miner_') or query.startswith('voter_'):
        return redirect(url_for('address_detail', address=query))
    # Check if it's a block number
    elif query.isdigit():
        try:
            with get_db() as db:
                with db.cursor() as cur:
                    cur.execute("SELECT hash FROM blocks WHERE id = %s", (query,))
                    block = cur.fetchone()
                    if block:
                        return redirect(url_for('block_detail', block_hash=block['hash']))
        except:
            pass

    flash("No results found for your search", 'warning')
    return redirect(url_for('blockchain'))

from datetime import datetime  # Add this at the top with other imports

# Add this right before your routes (but after app creation)
@app.context_processor
def inject_year():
    return {'current_year': datetime.now().year}

@app.template_filter('current_year')
def current_year_filter(s):
    return datetime.now().year

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)