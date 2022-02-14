/* Copyright (c) 2022 Pixel Flux
 *
 * Permission is hereby granted, free of charge, to any person obtaining
 * a copy of this software and associated documentation files (the
 * "Software"), to deal in the Software without restriction, including
 * without limitation the rights to use, copy, modify, merge, publish,
 * distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so, subject to
 * the following conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 * IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
 * CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
 * TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

#pragma once

#include "flecs.h"
#include "entity.hpp"


namespace pyflecs {

    class iter final {
    public:
        iter(ecs_iter_t iter);

        bool next();
        void* get_term_data(entity& e, int32_t idx);
        int32_t count()
        {
            return mRaw.count;
        }

        ecs_entity_t get_entity(size_t idx)
        {
            return mRaw.entities[idx];
        }

        int32_t term_count()
        {
            return mRaw.term_count;
        }

        ecs_term_t term(size_t idx)
        {
            return mRaw.terms[idx];
        }

        size_t term_size(size_t idx)
        {
            return ecs_term_size(&mRaw, idx);
        }

        bool term_owned(size_t idx)
        {
            return ecs_term_is_owned(&mRaw, idx);
        }

    private:
        ecs_iter_t mRaw;

    };
}